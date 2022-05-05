#!/usr/bin/env python3

import os
import tempfile
import json
import typer
from modules.core import Core
from modules.pdf import Pdf
from modules.metadata import Metadata
from modules.checks import path_checks, file_checks, dependencies_checks

app = typer.Typer()


@app.command()
def run(input_file: str,
        output_folder: str,
        metadata: str,
        compress: bool = True):
    # Destruction of the temporary directory on completion
    with tempfile.TemporaryDirectory() as tmp_dir:

        # Create core object instace
        core = Core(tmp_dir, output_folder)

        # Checks
        file_checks(input_file)
        file_checks(metadata)
        path_checks(output_folder)
        dependencies_checks()

        # Retrieve ISBN
        json_file = os.path.abspath(metadata)
        with open(json_file) as json_data:
            isbn = json.load(json_data)['isbn'].replace('-', '')

        # Create object instaces
        metadata = Metadata(isbn)
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
