from metadata import Book, Chapter


def test_book_access():
    book = Book("978-1-80064-779-4", "10.11647/OBP.0309",
                "The Merger Mystery", "monograph")
    assert book.isbn == "978-1-80064-779-4"
    assert book.doi == "10.11647/OBP.0309"
    assert book.title == "The Merger Mystery"
    assert book.type == "monograph"


def test_book_defaults():
    book = Book()
    assert book.isbn is None
    assert book.doi is None
    assert book.title is None
    assert book.type is None


def test_book_equality():
    book1 = Book("978-1-80064-779-4", "10.11647/OBP.0309",
                 "The Merger Mystery", "monograph")
    book2 = Book("978-1-80064-779-4", "10.11647/OBP.0309",
                 "The Merger Mystery", "monograph")
    assert book1 == book2


def test_book_inequality():
    book1 = Book("978-1-80064-779-4", "10.11647/OBP.0309",
                 "The Merger Mystery", "monograph")
    book2 = Book("978-1-80064-690-2", "10.11647/OBP.0295",
                 "Performing Deception", "monograph")
    assert book1 != book2


def test_book_from_dict():
    dict = {"isbn": "978-1-80064-779-4", "doi": "10.11647/OBP.0309",
            "title": "The Merger Mystery", "type": "monograph"}
    book = Book.from_dict(dict)
    assert book.isbn == dict.get("isbn")
    assert book.doi == dict.get("doi")
    assert book.title == dict.get("title")
    assert book.type == dict.get("type")


def test_chapter_access():
    chapter = Chapter("Brian Rappert",
                      "Preface: Attention, Attention, Attention!",
                      "In Performing Deception, Brian Rappert [...]",
                      "vii–xii",
                      "10.11647/obp.0295.09",
                      "https://creativecommons.org/licenses/by-nc/4.0/",
                      "Open Book Publishers")
    assert chapter.author == "Brian Rappert"
    assert chapter.title == "Preface: Attention, Attention, Attention!"
    assert chapter.abstract == "In Performing Deception, Brian Rappert [...]"
    assert chapter.pages == "vii–xii"
    assert chapter.doi == "10.11647/obp.0295.09"
    assert chapter.licence == "https://creativecommons.org/licenses/by-nc/4.0/"
    assert chapter.publisher == "Open Book Publishers"


def test_chapter_defaults():
    chapter = Chapter()
    assert chapter.author is None
    assert chapter.title is None
    assert chapter.abstract is None
    assert chapter.pages == []
    assert chapter.doi is None
    assert chapter.licence is None
    assert chapter.publisher is None


def test_chapter_equality():
    chapter1 = Chapter()
    chapter2 = Chapter()
    assert chapter1 == chapter2


def test_chapter_inequality():
    chapter1 = Chapter()
    chapter2 = Chapter("Brian Rappert",
                       "Preface: Attention, Attention, Attention!",
                       "In Performing Deception, Brian Rappert [...]",
                       "vii–xii",
                       "10.11647/obp.0295.09",
                       "https://creativecommons.org/licenses/by-nc/4.0/",
                       "Open Book Publishers")
    chapter1 != chapter2


def test_chapter_from_dict():
    dict = {"author": "Brian Rappert",
            "title": "Preface: Attention, Attention, Attention!",
            "abstract": "In Performing Deception, Brian Rappert [...]",
            "pages": "vii–xii",
            "doi": "10.11647/obp.0295.09",
            "licence": "https://creativecommons.org/licenses/by-nc/4.0/",
            "publisher": "Open Book Publishers"}
    chapter = Chapter.from_dict(dict)
    assert chapter.author == dict.get("author")
    assert chapter.title == dict.get("title")
    assert chapter.abstract == dict.get("abstract")
    assert chapter.pages == dict.get("pages")
    assert chapter.doi == dict.get("doi")
    assert chapter.licence == dict.get("licence")
    assert chapter.publisher == dict.get("publisher")


def test_chapter_to_dict():
    chapter = Chapter("Brian Rappert",
                      "Preface: Attention, Attention, Attention!",
                      "In Performing Deception, Brian Rappert [...]",
                      "vii–xii",
                      "10.11647/obp.0295.09",
                      "https://creativecommons.org/licenses/by-nc/4.0/",
                      "Open Book Publishers")
    dict = {"author": "Brian Rappert",
            "title": "Preface: Attention, Attention, Attention!",
            "abstract": "In Performing Deception, Brian Rappert [...]",
            "pages": "vii–xii",
            "doi": "10.11647/obp.0295.09",
            "licence": "https://creativecommons.org/licenses/by-nc/4.0/",
            "publisher": "Open Book Publishers"}
    assert chapter.to_dict() == dict
