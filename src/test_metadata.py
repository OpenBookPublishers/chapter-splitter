from metadata import Book


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
