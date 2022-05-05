#!/usr/bin/env python3

import os
import shutil
from zipfile import ZipFile


class Core:
    def __init__(self, tmp_dir, output_folder):
        self.tmp_dir = tmp_dir
        self.output_folder = output_folder

    def output_archive(self, doi_suffix):
        '''
        Output a zip archive to the user given output folder.

        The archive name looks like this: obp.0197.zip
        '''
        out_file = '{}/{}.zip'.format(self.output_folder,
                                      doi_suffix)
        suffix = '_original'
        files = filter(lambda w: not w.endswith(suffix),
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
                    shutil.copy2(pathname, self.output_folder)
