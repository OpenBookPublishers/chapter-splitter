#!/usr/bin/env python3

import argparse
from os import path
import sys
sys.path.append('modules')

from doi import Doi
from pdf import Pdf
from metadata import Metadata
from checks import path_checks, dependencies_checks


parser = argparse.ArgumentParser(description='chapter-splitter')

parser.add_argument('input_folder',
					help = 'Input folder where PDF files are located')
parser.add_argument('output_folder',
					help = 'Output folder where to store the new PDFs')
parser.add_argument('-d', '--doi',
					help = 'The DOI (at book-level) you wish to parse',
					required = True)

args = parser.parse_args()

# Check parsed arguments
path_checks(args.input_folder)
path_checks(args.output_folder)

# Check dependencies
dependencies_checks()

# Discover chapter-level DOIs of the supplied --doi value
d = Doi(args.doi)
ch_dois = d.discover_ch_dois()

m = Metadata()
p = Pdf(args.input_folder, args.output_folder)

for doi in ch_dois:
	# Gather metadata for 'doi'
	doi_metadata = m.gather_metadata(doi)

	# Produce the PDF
	page_list = p.get_page_list(doi_metadata['page_range'])
	output_file_name = doi.split('/')[1] + '.pdf'

	p.merge_pdfs(page_list, output_file_name)

	# Write metadata
	output_file_path = path.join(args.output_folder, output_file_name)
	m.write_metadata(doi_metadata, output_file_path)
