from crossref.restful import Works
from typing import Dict, List


class Crossref():
    """Crossref compatibilty layer"""
    def __init__(self):
        self.works = Works()

    def get_book(self, isbn: str) -> Dict:
        """Return the book data associated to the supplied ISBN"""
        query = self.works.filter(isbn=isbn.replace('-', '')) \
                          .select('title', 'DOI', 'type')
        result = [x for x in query]
        data = {"title": result[0].get("title")[0],
                "doi":   result[0].get("DOI"),
                "type":  result[0].get("type"),
                "isbn":  isbn}
        return data

    def get_chapters(self, book: Dict) -> List:
        """Returns a chapter data related to the book"""
        query = self.works.filter(container_title=book.title,
                                  type='book-chapter') \
                          .select('DOI', 'license', 'author',
                                  'title', 'type', 'page',
                                  'publisher', 'abstract')

        # Assert that at least one DOI have been discovered
        if not query:
            raise AssertionError('Couldn\'t find any chapter-level DOIs'
                                 + ' for the supplied --isbn value')

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
