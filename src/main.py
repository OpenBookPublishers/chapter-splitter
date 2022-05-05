#!/usr/bin/env python3

import os
import tempfile
import json
import typer
from pathlib import Path
from modules.core import Core
from modules.pdf import Pdf
from modules.metadata import Metadata
from api import Book

app = typer.Typer()


@app.command()
def run(input_file:    Path = typer.Option("./file.pdf",
                                           exists=True, resolve_path=True),
        output_folder: Path = typer.Option("./output/",
                                           exists=True, resolve_path=True),
        metadata: typer.FileText = typer.Option("./metadata.json",
                                                exists=True),
        compress:      bool = True):

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Create core object instace
        core = Core(tmp_dir, output_folder)

        metadata_json = json.load(metadata)
        isbn = metadata_json.get("isbn")
        doi = metadata_json.get("doi")

        book = Book(isbn, doi)

        # Create object instaces
        metadata = Metadata(book.isbn.replace('-', ''))
        pdf = Pdf(input_file, tmp_dir)

        # Iterate over chapters metadata
        for chapter_data in metadata.chapters_data:
            page_range = chapter_data['page'].split('-')
            output_file_name = chapter_data['DOI'].split('/')[1] + '.pdf'

            # Merge PDFs
            pdf.merge_pdfs(page_range, output_file_name)

            # Write metadata
            output_file_path = os.path.join(tmp_dir, output_file_name)
            metadata.write_metadata(chapter_data, output_file_path)

        # PDFs are temporarely stored in tmp_dir
        if compress:
            # Output a zip archive
            core.output_archive(metadata.get_doi_suffix())
        else:
            # Output loose PDFs
            core.output_pdfs()


if __name__ == '__main__':
    typer.run(run)
