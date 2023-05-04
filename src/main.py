#!/usr/bin/env python3

import os
import tempfile
import typer
from pathlib import Path
from pdf import Pdf
from metadata import Metadata
from shutil import copy2
import re

app = typer.Typer()


@app.command()
def run(input_file:    Path = typer.Option("./file.pdf",
                                           exists=True, resolve_path=True),
        output_folder: Path = typer.Option("./output/",
                                           exists=True, resolve_path=True),
        doi:            str = typer.Argument(...),
        database:       str = "thoth"):

    with tempfile.TemporaryDirectory() as tmp_dir:

        metadata = Metadata(database, doi=doi)

        # Create object instaces
        pdf = Pdf(input_file, tmp_dir)

        # Iterate over chapters metadata
        for chapter in metadata.get_chapters():
            page_range = re.split('-|–', chapter.get("pages"))

            doi_fragments = chapter.get("doi").split('/')
            output_file_name = doi_fragments[-1].lower() + '.pdf'

            # Merge PDFs
            pdf.merge_pdfs(page_range, output_file_name)

            # Write metadata
            output_file_path = os.path.join(tmp_dir, output_file_name)
            metadata.write_metadata(chapter, output_file_path)

            # copy file to output dir
            copy2(output_file_path, output_folder)


if __name__ == '__main__':
    typer.run(run)
