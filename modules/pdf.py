#!/usr/bin/env python3

from subprocess import check_output, run
from pdfrw import PdfReader
from pagelabels import PageLabels
from os import path
from config import Config

class Pdf:
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder

        config = Config()
        self.cover_page_n = config.get_config('pdf', 'cover_page_n')
        self.copyright_page_n = config.get_config('pdf',
                                                  'copyright_page_n')

        self.page_one = self.get_page_one()

    def get_page_one(self):
        reader = PdfReader(self.input_file)
        labels = PageLabels.from_pdf(reader)

        '''
        The PageLabel tuple looks like this:

        PageLabelScheme(startpage=16,
                        style='arabic',
                        prefix='',
                        firstpagenum=1)
        '''
        for label in labels:
            if label[1] == 'arabic':
                return label[0]

    def get_page_range(self, page_range):
        ## Returns a list of the effective chapter page range

        # Convert the page numbers to int object type
        page_range = [int(page) + self.page_one for page in page_range]
        return page_range

    def merge_pdfs(self, page_list, output_file_name):
        ## Executes the command to merge the PDF files

        cmd = ['pdfunite']
        cmd.append(path.join(self.input_folder, self.cover_file_name))
        cmd.append(path.join(self.input_folder, self.copyright_file_name))
        cmd.extend([path.join(self.input_folder, value) \
                    for value in page_list])
        cmd.append(path.join(self.output_folder, output_file_name))

        run(cmd)
        print('{}: Created' \
              .format(output_file_name))
