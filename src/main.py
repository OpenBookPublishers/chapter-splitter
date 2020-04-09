#!/usr/bin/env python3

from os import path, listdir
import tempfile
from zipfile import ZipFile
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
    output_file_path = path.join(output_dir, output_file_name)
    Metadata.write_metadata(doi_metadata, output_file_path)


def get_tmp_dir():
    return tempfile.mkdtemp()


def run():

    # Create an instance of the core objectxs
    core = Core()

    out_dir = core.argv.output_folder
    tmp_dir = out_dir if not core.argv.compress else get_tmp_dir()

    # Check parsed arguments
    file_checks(core.argv.input_file)
    path_checks(out_dir)

    # Check dependencies
    dependencies_checks()

    metadata = Metadata(core.argv.isbn)
    ch_dois = metadata.get_ch_dois()
    p = Pdf(core.argv.input_file, tmp_dir)

    for doi in ch_dois:
        do_split(metadata, p, tmp_dir, doi)

    if core.argv.compress:
        out_file = '{}/{}.zip'.format(out_dir, metadata.get_doi_suffix())
        suffix = '_original'
        files = filter(lambda w: not w.endswith(suffix), listdir(tmp_dir))
        with ZipFile(out_file, 'w') as zipfile:
            for file in files:
                zipfile.write('{}/{}'.format(tmp_dir, file), file)


if __name__ == '__main__':
    run()
