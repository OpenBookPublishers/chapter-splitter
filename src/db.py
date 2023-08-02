from crossref.restful import Works
from thothlibrary import ThothClient
from urllib.parse import urljoin
import json
import requests
from os import getenv
from typing import Dict, List


class Db():
    """Base Db class to derive specialised database classes from"""

    def __init__(self, doi: str) -> None:
        self.db = self.init_db()
        self.doi = urljoin('https://doi.org/', doi)

    def init_db(self):
        """Init database object"""
        raise NotImplementedError

    def get_book(self):
        """Return book data"""
        raise NotImplementedError

    def get_chapters(self):
        """Return chapters data"""
        raise NotImplementedError


class Crossref(Db):
    """Crossref compatibility layer"""
    def init_db(self):
        """Init database object"""
        return Works()

    def get_book(self) -> Dict:
        """Return book data"""
        query = self.db.doi(self.doi)

        if not query:
            raise ValueError(f"No book data associated to the DOI {self.doi}"
                             "found on the database Crossref")

        data = {"title": query.get("title")[0],
                "doi":   query.get("DOI")}
        return data

    def get_chapters(self, book: Dict) -> List:
        """Return chapters data"""
        query = self.db.filter(container_title=book.get("title"),
                               type='book-chapter') \
                       .select('DOI', 'license', 'author',
                               'title', 'type', 'page',
                               'publisher', 'abstract')

        if not query:
            raise ValueError("No chapter data associated to the DOI"
                             f"{self.doi} found on the database Crossref")

        chapters = []
        for chapter in query:
            data = {"doi":       chapter.get("DOI"),
                    "author":    self.join_author_names(chapter),
                    "title":     chapter.get("title")[0],
                    "publisher": chapter.get("publisher"),
                    "abstract":  chapter.get("abstract"),
                    "pages":     chapter.get("page"),
                    "licence":   chapter.get("license")[0]['URL']}
            chapters.append(data)

        return chapters

    def join_author_names(self, chapter_data: Dict) -> str:
        """Returns a string with author names, separated by semicolon"""
        author_list = []

        for author in chapter_data.get("author"):
            # do not assume we know author's first name
            full_name = [author.get("given", ""), author.get("family", "")]
            author_list.append(" ".join(full_name).strip())

        return '; '.join(author_list)


class Thoth(Db):
    """Thoth compatibility layer"""

    def init_db(self):
        """Init database object"""
        return ThothClient()

    def get_book(self) -> Dict:
        """Return book data"""
        work = self.db.work_by_doi(doi=self.doi, raw=True)
        work_dict = json.loads(work)['data']['workByDoi']

        data = {"title": work_dict.get("fullTitle"),
                "doi":   self.doi}
        return data

    def get_chapters(self, book: Dict) -> List:
        """Return chapters data"""
        # TODO replace this with a Thoth library method when available
        url = 'https://api.thoth.pub/graphql'
        query = {"query": """{ workByDoi (doi: "%s") {
                                relations(relationTypes: HAS_CHILD) {
                                    relatedWork {
                                        workId
                                        fullTitle
                                        copyrightHolder
                                        longAbstract
                                        pageInterval
                                        doi
                                        license
                                        imprint {
                                            imprintName
                                            }
                                        }
                                    }
                                }
                             }""" % book.get("doi")}

        try:
            r = requests.post(url, json=query)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        r_dict = json.loads(r.text)

        chapters = []
        for relatedWork in r_dict['data']['workByDoi']['relations']:
            work = relatedWork.get("relatedWork", {})
            data = {"doi":       work.get("doi"),
                    "author":    work.get("copyrightHolder"),
                    "title":     work.get("fullTitle"),
                    "publisher": work.get("imprint", {}).get("imprintName"),
                    "abstract":  work.get("longAbstract"),
                    "pages":     work.get("pageInterval"),
                    "licence":   work.get("license"),
                    "workId":    work.get("workId")}
            chapters.append(data)

        return chapters

    def write_urls(self, chapter):
        """Write Landing Page and Full Text URLs to Thoth"""
        chapter_doi = chapter.get("doi").split('/')[-1].lower()
        book_doi = chapter_doi.rpartition('.')[0]
        landing_page_root = (
            'https://www.openbookpublishers.com/books/10.11647/'
            '{book_doi}/chapters/10.11647/{chapter_doi}')
        full_text_url_root = (
            'https://books.openbookpublishers.com/10.11647/'
            '{chapter_doi}.pdf')

        username = getenv('THOTH_EMAIL')
        password = getenv('THOTH_PWD')
        if username is None:
            raise KeyError(
                'No Thoth username provided '
                '(THOTH_EMAIL environment variable not set)')
        if password is None:
            raise KeyError(
                'No Thoth password provided '
                '(THOTH_PWD environment variable not set)')

        self.db.login(username, password)

        publication = {"workId":          chapter.get("workId"),
                       "publicationType": "PDF",
                       "isbn":            None,
                       "widthMm":         None,
                       "widthIn":         None,
                       "heightMm":        None,
                       "heightIn":        None,
                       "depthMm":         None,
                       "depthIn":         None,
                       "weightG":         None,
                       "weightOz":        None}
        publication_id = self.db.create_publication(publication)

        location = {"publicationId":    publication_id,
                    "landingPage":      landing_page_root.format(
                        book_doi=book_doi, chapter_doi=chapter_doi),
                    "fullTextUrl":      full_text_url_root.format(
                        book_doi=book_doi, chapter_doi=chapter_doi),
                    "locationPlatform": "OTHER",
                    "canonical":        "true"}
        self.db.create_location(location)

        print('{}: URLs written to Thoth'.format(chapter_doi))
