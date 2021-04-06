#!/usr/bin/env python3

from os import path
from .config import Config
import fitz

class Pdf:
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder

        config = Config()
        self.cover_page_n = config.get_config('pdf', 'cover_page_n')
        self.copyright_page_n = config.get_config('pdf', 'copyright_page_n')

    def merge_pdfs(self, page_range, output_file_name):
        """
        Create the chapter PDF by merging toghether extracts of the original 
        PDF. These parts are front cover, copyright page and chapter body text.
        """
        
        original_pdf = fitz.open(self.input_file)
        real_page_range = [original_pdf.get_page_numbers(p, only_one=True)[0]
                           for p in page_range]

        chapter_pdf = fitz.open()

        # cover
        chapter_pdf.insert_pdf(original_pdf,
                               to_page = int(self.cover_page_n))
        # copyright page
        chapter_pdf.insert_pdf(original_pdf,
                               from_page = int(self.copyright_page_n),
                               to_page = int(self.copyright_page_n))
        # chapter body
        chapter_pdf.insert_pdf(original_pdf,
                               from_page = int(real_page_range[0]),
                               to_page = int(real_page_range[1]))
        
        chapter_pdf.save(path.join(self.output_folder, output_file_name))

        original_pdf.close()
        chapter_pdf.close()

        print('{}: Created'.format(output_file_name))
