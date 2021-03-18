#!/usr/bin/env python3

from pdfrw import PdfReader
from pagelabels import PageLabels
from os import path
from .config import Config
import roman
import fitz

class Pdf:
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder

        config = Config()
        self.cover_page_n = int(config.get_config('pdf', 'cover_page_n'))
        self.copyright_page_n = int(config.get_config('pdf',
                                                  'copyright_page_n'))

        self.page_one = self.get_page_one()

    def get_page_one(self):
        '''
          The PageLabel tuple looks like this:

          PageLabelScheme(startpage=16,
                          style='arabic',
                          prefix='',
                          firstpagenum=1)
        '''
        reader = PdfReader(self.input_file)
        labels = PageLabels.from_pdf(reader)

        for label in labels:
            if label[1] == 'arabic':
                return label[0] - 1

    def get_page_range(self, page_range):
        """
        Returns a list of the effective chapter page range
        """

        # Check if the page range is numeric or roman numeral
        if page_range[0].isnumeric() and page_range[1].isnumeric():
            # Convert the page numbers to int object type
            page_range = [int(page) + self.page_one for page in page_range]
        else:
            # Convert pages to arabic numeral
            page_range = [roman.fromRoman(page.upper())
                          for page in page_range]
        return page_range

    def merge_pdfs(self, page_range, output_file_name):
        """
        Executes the command to merge the PDF files
        """

        original_pdf = fitz.open(self.input_file)

        chapter_pdf = fitz.open()
        chapter_pdf.insert_pdf(original_pdf,
                               to_page = self.cover_page_n)
        chapter_pdf.insert_pdf(original_pdf,
                               from_page = self.copyright_page_n,
                               to_page = self.copyright_page_n)
        chapter_pdf.insert_pdf(original_pdf,
                               from_page = page_range[0],
                               to_page = page_range[1])
        chapter_pdf.save(path.join(self.output_folder, output_file_name))

        original_pdf.close()
        chapter_pdf.close()

        print('{}: Created'.format(output_file_name))
