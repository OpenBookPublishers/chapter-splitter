import sys
from types import ModuleType
from pathlib import Path

from typer.testing import CliRunner


pdf_module = ModuleType("pdf")
pdf_module.Pdf = object
metadata_module = ModuleType("metadata")
metadata_module.Metadata = object
original_pdf_module = sys.modules.get("pdf")
original_metadata_module = sys.modules.get("metadata")
sys.modules["pdf"] = pdf_module
sys.modules["metadata"] = metadata_module

import main

if original_pdf_module is None:
    sys.modules.pop("pdf", None)
else:
    sys.modules["pdf"] = original_pdf_module

if original_metadata_module is None:
    sys.modules.pop("metadata", None)
else:
    sys.modules["metadata"] = original_metadata_module


runner = CliRunner()


def test_cli_help_lists_write_urls_toggle():
    result = runner.invoke(main.app, ["--help"])

    assert result.exit_code == 0
    assert "--write-urls / --no-write-urls" in result.stdout


def test_cli_runs_with_write_urls_flag(monkeypatch, tmp_path):
    calls = {"write_urls": []}
    input_file = tmp_path / "book.pdf"
    output_folder = tmp_path / "output"
    input_file.write_bytes(b"%PDF-1.4\n")
    output_folder.mkdir()

    class MockPdf:
        def __init__(self, source, tmp_dir):
            self.tmp_dir = Path(tmp_dir)
            calls["pdf_init"] = (source, self.tmp_dir)

        def merge_pdfs(self, page_range, output_file_name):
            calls["merge_pdfs"] = (page_range, output_file_name)
            (self.tmp_dir / output_file_name).write_bytes(b"%PDF-1.4\n")

    class MockMetadata:
        def __init__(self, database, doi):
            calls["metadata_init"] = (database, doi)

        def get_chapters(self):
            return [
                {
                    "pages": "1-2",
                    "doi": "10.11647/obp.0309.01",
                    "workId": "work-1",
                }
            ]

        def write_metadata(self, chapter, output_file_path):
            calls["write_metadata"] = (chapter, output_file_path)

        def write_urls(self, chapter):
            calls["write_urls"].append(chapter)

    monkeypatch.setattr(main, "Pdf", MockPdf)
    monkeypatch.setattr(main, "Metadata", MockMetadata)

    result = runner.invoke(
        main.app,
        [
            "--input-file",
            str(input_file),
            "--output-folder",
            str(output_folder),
            "--write-urls",
            "10.11647/obp.0309",
        ],
    )

    assert result.exit_code == 0
    assert calls["metadata_init"] == ("thoth", "10.11647/obp.0309")
    assert calls["merge_pdfs"] == (["1", "2"], "obp.0309.01.pdf")
    assert calls["write_urls"] == [
        {
            "pages": "1-2",
            "doi": "10.11647/obp.0309.01",
            "workId": "work-1",
        }
    ]
