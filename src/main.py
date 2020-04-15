#!/usr/bin/env python3

import os
import tempfile
from modules.core import Core
from modules.pdf import Pdf
from modules.metadata import Metadata
from modules.checks import path_checks, file_checks, dependencies_checks


def do_split(m, p, output_dir, doi):
    # Gather metadata for 'doi'
    doi_metadata = m.gather_metadata(doi)

    # Produce the PDF
    page_range = p.get_page_range(doi_metadata['page_range'])
    output_file_name = doi.split('/')[1] + '.pdf'

    p.merge_pdfs(page_range, output_file_name)

    # Write metadata
    output_file_path = os.path.join(output_dir, output_file_name)
    Metadata.write_metadata(doi_metadata, output_file_path)


def run():

    # Destruction of the temporary directory on completion
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create an instance of the core objects
        core = Core(tmp_dir)

        # Check parsed arguments
        file_checks(core.argv.input_file)
        path_checks(core.argv.output_folder)

        # Check dependencies
        dependencies_checks()

        metadata = Metadata(core.argv.isbn)
        ch_dois = metadata.get_ch_dois()
        p = Pdf(core.argv.input_file, tmp_dir)

        for doi in ch_dois:
            do_split(metadata, p, tmp_dir, doi)

        # PDFs are temporarely stored in tmp_dir
        if core.argv.compress:
            # output a zip archive
            core.output_archive(metadata.get_doi_suffix())
        else:
            # output loose PDFs
            core.output_pdfs()


if __name__ == '__main__':
    run()
