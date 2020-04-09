#!/usr/bin/env python3

import argparse

class Core:
    def __init__(self):
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

        parser.add_argument('-i', '--isbn',
                            help='A valid ISBN of the edition',
                            required=True)

        return parser.parse_args()
