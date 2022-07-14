from metadata import Book, Chapter


def test_book_access():
    book = Book("10.11647/OBP.0309", "The Merger Mystery")
    assert book.doi == "10.11647/OBP.0309"
    assert book.title == "The Merger Mystery"


def test_book_defaults():
    book = Book()
    assert book.doi is None
    assert book.title is None


def test_book_equality():
    book1 = Book("10.11647/OBP.0309", "The Merger Mystery")
    book2 = Book("10.11647/OBP.0309", "The Merger Mystery")
    assert book1 == book2


def test_book_inequality():
    book1 = Book("10.11647/OBP.0309", "The Merger Mystery")
    book2 = Book("10.11647/OBP.0295", "Performing Deception")
    assert book1 != book2


def test_book_from_dict():
    dict = {"doi": "10.11647/OBP.0309", "title": "The Merger Mystery"}
    book = Book.from_dict(dict)
    assert book.doi == dict.get("doi")
    assert book.title == dict.get("title")


def test_book_to_dict():
    book = Book("10.11647/OBP.0309", "The Merger Mystery")
    dict = {"doi": "10.11647/OBP.0309", "title": "The Merger Mystery"}
    assert book.to_dict() == dict


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
