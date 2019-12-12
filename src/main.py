#!/usr/bin/env python3

import argparse
from os import path, listdir
import tempfile
from zipfile import ZipFile
from modules.doi import Doi
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
    parser = argparse.ArgumentParser(description='chapter-splitter')

    parser.add_argument('input_file',
                        help='PDF file to elaborate')
    parser.add_argument('output_folder',
                        help='Output folder where to store the new PDFs')
    parser.add_argument('-d', '--doi',
                        help='The DOI (at book-level) you wish to parse',
                        required=True)
    parser.add_argument('-c', '--compress-output', dest='compress',
                        action='store_true',
                        help='If set it will output a single zip file')

    args = parser.parse_args()

    out_dir = args.output_folder
    tmp_dir = out_dir if not args.compress else get_tmp_dir()

    # Check parsed arguments
    file_checks(args.input_file)
    path_checks(out_dir)

    # Check dependencies
    dependencies_checks()

    # Discover chapter-level DOIs of the supplied --doi value
    d = Doi(args.doi.lower())
    ch_dois = d.discover_ch_dois()

    m = Metadata()
    p = Pdf(args.input_file, tmp_dir)

    for doi in ch_dois:
        do_split(m, p, tmp_dir, doi)

    if args.compress:
        out_file = '{}/{}.zip'.format(out_dir, d.book_level_doi_suffix)
        suffix = '_original'
        files = filter(lambda w: not w.endswith(suffix), listdir(tmp_dir))
        with ZipFile(out_file, 'w') as zipfile:
            for file in files:
                zipfile.write('{}/{}'.format(tmp_dir, file), file)


if __name__ == '__main__':
    run()
