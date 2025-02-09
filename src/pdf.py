#!/usr/bin/env python3

from os import path, environ
import fitz
from roman import fromRoman


class Pdf:
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder

        self.cover_page_n = environ.get('COVER_PAGE', 0)
        self.copyright_page_n = environ.get('COPYRIGHT_PAGE', 4)

    def merge_pdfs(self, page_range, output_file_name):
        """Compose a PDF by merging sections together

        Create the chapter PDF by merging together extracts of the original
        PDF. These parts are front cover, copyright page and chapter body text.
        """

        try:
            original_pdf = fitz.open(self.input_file)
            try:
                real_page_range = [original_pdf.get_page_numbers(p, only_one=True)[0]
                                   for p in page_range]
            except IndexError:
                print(f"Error: Could not find page labels for page_range: {page_range}")
                print(f"Original PDF page count: {len(original_pdf)}")
                raise

            chapter_pdf = fitz.open()
            labels = []

            # cover
            if self.cover_page_n:
                chapter_pdf.insert_pdf(original_pdf,
                                       to_page=int(self.cover_page_n))
                labels.append({'startpage': 0, 'style': 'A',
                               'firstpagenum': int(self.cover_page_n)})

            # copyright page
            if self.copyright_page_n:
                chapter_pdf.insert_pdf(original_pdf,
                                       from_page=int(self.copyright_page_n),
                                       to_page=int(self.copyright_page_n))
                labels.append({'startpage': 1, 'style': 'r',
                               'firstpagenum': int(self.copyright_page_n)})

            # chapter body
            chapter_pdf.insert_pdf(original_pdf,
                                   from_page=int(real_page_range[0]),
                                   to_page=int(real_page_range[1]))

            if page_range[0].isnumeric():
                chapter_page = int(page_range[0])
                chapter_style = 'D'
            else:
                chapter_page = fromRoman(page_range[0].upper())
                chapter_style = 'r'

            labels.append({'startpage': 2, 'style': chapter_style,
                           'firstpagenum': chapter_page})

            # Update page labels
            chapter_pdf.set_page_labels(labels)

            chapter_pdf.save(path.join(self.output_folder, output_file_name))

            original_pdf.close()
            chapter_pdf.close()

            print('{}: Created'.format(output_file_name))
        except (IndexError, ValueError, TypeError, OSError, FileNotFoundError,
                fitz.FileDataError, fitz.EmptyFileError, fitz.FileNotFoundError):
            print(self.__dict__)
            raise
