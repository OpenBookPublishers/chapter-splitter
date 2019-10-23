#!/usr/bin/env python3

import argparse
from os import path
import sys
sys.path.append('modules')

from doi import Doi
from pdf import Pdf
from metadata import Metadata
from checks import path_checks, file_checks, dependencies_checks


def do_split(m, p, output_dir, doi):
    # Gather metadata for 'doi'
    doi_metadata = m.gather_metadata(doi)

    # Produce the PDF
    page_range = p.get_page_range(doi_metadata['page_range'])
    output_file_name = doi.split('/')[1] + '.pdf'

    p.merge_pdfs(page_range, output_file_name)

    # Write metadata
    output_file_path = path.join(output_dir, output_file_name)
    m.write_metadata(doi_metadata, output_file_path)


def run():
    parser = argparse.ArgumentParser(description='chapter-splitter')

    parser.add_argument('input_file',
                        help = 'PDF file to elaborate')
    parser.add_argument('output_folder',
                        help = 'Output folder where to store the new PDFs')
    parser.add_argument('-d', '--doi',
                        help = 'The DOI (at book-level) you wish to parse',
                        required = True)

    args = parser.parse_args()

    # Check parsed arguments
    file_checks(args.input_file)
    path_checks(args.output_folder)

    # Check dependencies
    dependencies_checks()

    # Discover chapter-level DOIs of the supplied --doi value
    d = Doi(args.doi)
    ch_dois = d.discover_ch_dois()

    m = Metadata()
    p = Pdf(args.input_file, args.output_folder)

    for doi in ch_dois:
        do_split(m, p, args.output_folder, doi)

if __name__ == '__main__':
    run()
