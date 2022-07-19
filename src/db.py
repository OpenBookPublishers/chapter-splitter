from crossref.restful import Works
from thothlibrary import ThothClient
from urllib.parse import urljoin
import json
import requests
from typing import Dict, List


class Crossref():
    """Crossref compatibilty layer"""
    def __init__(self, doi: str):
        self.works = Works()
        self.doi = urljoin('https://doi.org/', doi)

    def get_book(self) -> Dict:
        """Return the book data associated to the supplied ISBN"""
        query = self.works.doi(self.doi)

        if not query:
            raise ValueError(f"No book data associated to the DOI {self.doi}"
                             "found on the database Crossref")

        data = {"title": query.get("title")[0],
                "doi":   query.get("DOI")}
        return data

    def get_chapters(self, book: Dict) -> List:
        """Returns a chapter data related to the book"""
        query = self.works.filter(container_title=book.get("title"),
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


class Thoth():
    """Thoth compatibilty layer"""
    def __init__(self, doi: str):
        self.thoth = ThothClient()
        self.doi_url = urljoin('https://doi.org/', doi)

    def get_book(self) -> Dict:
        work = self.thoth.work_by_doi(doi=self.doi_url, raw=True)
        work_dict = json.loads(work)['data']['workByDoi']

        data = {"title": work_dict.get("fullTitle"),
                "doi":   self.doi_url}
        return data

    def get_chapters(self, book: Dict) -> List:
        # TODO replace this with a Thoth library method when available
        url = 'https://api.thoth.pub/graphql'
        query = {"query": """{ workByDoi (doi: "%s") {
                                relations(relationTypes: HAS_CHILD) {
                                    relatedWork {
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
                    "licence":   work.get("license")}
            chapters.append(data)

        return chapters
