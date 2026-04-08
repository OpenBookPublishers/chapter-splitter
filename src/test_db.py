from types import SimpleNamespace

from db import Thoth


def test_thoth_get_book_uses_canonical_title(monkeypatch):
    class MockDb:
        def work_by_doi(self, doi):
            assert doi == "https://doi.org/10.11647/obp.0309"
            return SimpleNamespace(
                titles=[
                    SimpleNamespace(
                        canonical=False,
                        fullTitle="Fallback Title",
                        title="Fallback Title",
                    ),
                    SimpleNamespace(
                        canonical=True,
                        fullTitle="Canonical Title",
                        title="Canonical Title",
                    ),
                ]
            )

    monkeypatch.setattr(Thoth, "init_db", lambda self: MockDb())

    db = Thoth("10.11647/obp.0309")

    assert db.get_book() == {
        "title": "Canonical Title",
        "doi": "https://doi.org/10.11647/obp.0309",
    }


def test_thoth_get_page_range_falls_back_to_first_and_last_page():
    assert Thoth.get_page_range(
        {"pageInterval": None, "firstPage": "11", "lastPage": "20"}
    ) == "11-20"


def test_thoth_get_page_range_uses_single_page_when_needed():
    assert Thoth.get_page_range(
        {"pageInterval": None, "firstPage": "7", "lastPage": None}
    ) == "7-7"


def test_thoth_write_urls_uses_pat_and_preserves_payloads(monkeypatch):
    class MockDb:
        def __init__(self):
            self.token = None
            self.publication = None
            self.location = None

        def set_token(self, token):
            self.token = token

        def create_publication(self, publication):
            self.publication = publication
            return "publication-1"

        def create_location(self, location):
            self.location = location

    mock_db = MockDb()
    monkeypatch.setattr(Thoth, "init_db", lambda self: mock_db)
    monkeypatch.setenv("THOTH_PAT", "test-pat")

    db = Thoth("10.11647/obp.0309")
    db.write_urls(
        {
            "doi": "https://doi.org/10.11647/obp.0309.01",
            "workId": "work-1",
        }
    )

    assert mock_db.token == "test-pat"
    assert mock_db.publication == {
        "workId": "work-1",
        "publicationType": "PDF",
        "isbn": None,
        "widthMm": None,
        "widthIn": None,
        "heightMm": None,
        "heightIn": None,
        "depthMm": None,
        "depthIn": None,
        "weightG": None,
        "weightOz": None,
    }
    assert mock_db.location == {
        "publicationId": "publication-1",
        "landingPage": (
            "https://www.openbookpublishers.com/books/10.11647/obp.0309/"
            "chapters/10.11647/obp.0309.01"
        ),
        "fullTextUrl": "https://books.openbookpublishers.com/10.11647/obp.0309.01.pdf",
        "locationPlatform": "OTHER",
        "canonical": "true",
    }
