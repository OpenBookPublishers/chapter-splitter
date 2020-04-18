#!/usr/bin/env python3

import os
import tempfile
from modules.core import Core
from modules.pdf import Pdf
from modules.metadata import Metadata
from modules.checks import path_checks, file_checks, dependencies_checks


def run():
    # Destruction of the temporary directory on completion
    with tempfile.TemporaryDirectory() as tmp_dir:

        # Create core object instace
        core = Core(tmp_dir)

        # Checks
        file_checks(core.argv.input_file)
        path_checks(core.argv.output_folder)
        dependencies_checks()

        # Create object instaces
        metadata = Metadata(core.argv.isbn)
        pdf = Pdf(core.argv.input_file, tmp_dir)

        # Iterate over chapters metadata
        for chapter_data in metadata.get_chapters_data():
            # Produce the PDF
            page_range = pdf.get_page_range(chapter_data['page'].split('-'))
            output_file_name = chapter_data['DOI'].split('/')[1] + '.pdf'

            pdf.merge_pdfs(page_range, output_file_name)

            # Write metadata
            output_file_path = os.path.join(tmp_dir, output_file_name)
            Metadata.write_metadata(chapter_data, output_file_path)

        # PDFs are temporarely stored in tmp_dir
        if core.argv.compress:
            # Output a zip archive
            core.output_archive(metadata.get_doi_suffix())
        else:
            # Output loose PDFs
            core.output_pdfs()


if __name__ == '__main__':
    run()
