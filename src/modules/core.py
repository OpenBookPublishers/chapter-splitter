#!/usr/bin/env python3

import argparse
import os
import shutil
from zipfile import ZipFile


class Core:
    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir

        # Parse arguments
        self.argv = self.parse_args()

    def parse_args(self, argv=None):
        '''
        Parse input arguments with argparse. 
        Return argparse object.
        '''

        parser = argparse.ArgumentParser(description='chapter-splitter')

        parser.add_argument('input_file',
                            help='PDF file to elaborate')

        parser.add_argument('output_folder',
                            help='Output folder where to store the new PDFs')

        parser.add_argument('-c', '--compress-output', dest='compress',
                            action='store_true',
                            help='If set it will output a single zip file')

        return parser.parse_args()

    def output_archive(self, doi_suffix):
        '''
        Output a zip archive to the user given output folder.

        The archive name looks like this: obp.0197.zip
        '''
        out_file = '{}/{}.zip'.format(self.argv.output_folder,
                                      doi_suffix)
        suffix = '_original'
        files = filter(lambda w: not w.endswith(suffix), \
                       os.listdir(self.tmp_dir))
        with ZipFile(out_file, 'w') as zipfile:
            for file in files:
                zipfile.write('{}/{}'.format(self.tmp_dir, file), file)

    def output_pdfs(self):
        '''
        Output loose PDFs to the user given output folder.

        PDF files are name like this: obp.0197.01.pdf
        '''
        for basename in os.listdir(self.tmp_dir):
            if basename.endswith('.pdf'):
                pathname = os.path.join(self.tmp_dir, basename)
                if os.path.isfile(pathname):
                    shutil.copy2(pathname, self.argv.output_folder)
