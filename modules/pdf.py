#!/usr/bin/env python3

from subprocess import check_output, run
from os import path
from config import Config

class Pdf:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

        config = Config()
        self.cover_file_name = config.get_config('pdf',
                                                 'cover_file_name')
        self.copyright_file_name = config.get_config('pdf',
                                                     'copyright_file_name')

        self.file_list = self.get_file_list()

    def get_file_list(self):
        ## Returns a list of the file names stored in self.in_folder

        folder_content = check_output(['ls', '-v1',
                                       '-I', self.cover_file_name,
                                       '-I', self.copyright_file_name,
                                       self.input_folder])
        file_list = str(folder_content, 'utf-8').split('\n')

        # For convenience, insert an empty item at file_list[0],
        # so that the file name of page 1 is at file_list[1]
        file_list.insert(0, '')
        return file_list

    def get_page_list(self, page_range):
        ## Returns a list of the file names in the range page_range

        # Convert the page numbers to int object type
        page_range = [int(page) for page in page_range]

        return [value for counter, value in enumerate(self.file_list) \
                if (page_range[0] <= counter <= page_range[1])]

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
