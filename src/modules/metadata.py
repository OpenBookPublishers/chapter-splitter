#!/usr/bin/env python3

import json
from os import path
from datetime import datetime
from subprocess import run
import requests
from .config import Config
from crossref.restful import Works


class Metadata:
    def __init__(self, isbn):
        config = Config()
        self.api_url = config.get_config('metadata', 'api_url')
        self.works = Works()
        self.isbn = isbn
        self.book_metadata = self.get_book_metadata()

    def get_book_metadata(self):
        '''
        Get book metadata, which include all the entries
        associated to the supplied ISBN
        (i.e. type: book, book-chapter)
        '''

        return self.works.filter(isbn=self.isbn) \
                         .select('DOI', 'license', 'author',
                                 'title', 'type', 'page')

    def get_ch_dois(self):
        '''
        Discovers chapter DOIs by querying Crossref against the
        supplied ISBN value. Returns a python list with the
        'chapter level' DOIs.
        '''

        print('Start discovery of chapter-level DOIs')

        ch_dois = [item['DOI'] \
                   for item in self.book_metadata \
                   if item['type'] == 'book-chapter']

        # Assert that at least one DOI have been discovered
        if not ch_dois:
            raise AssertionError('Couldn\'t find any chapter-level DOIs'
                                 + ' for the supplied --isbn value')

        return ch_dois

    def get_doi_suffix(self):
        '''
        Return the book DOI suffix (string)
        '''

        book_types = ['monograph', 'edited-book']

        book_doi = [item['DOI'] \
                    for item in self.book_metadata \
                    if item['type'] in book_types]

        if not book_doi:
            raise AssertionError('Couldn\'t find book DOI')

        return book_doi[0].split('/')[1]

    def gather_metadata(self, doi):
        """
        Returns a dictionary filled with metadata of doi
        """

        json_data = self.get_json_data(doi)

        metadata = {'publisher_name': json_data['message']['publisher'],
                    'licence_url': json_data['message']['license'][0]['URL'],
                    'page_range': json_data['message']['page'].split('-'),
                    'book_title': json_data['message']['container-title'][0],
                    'chapter_title': json_data['message']['title'][0],
                    'author_name_0': Metadata.get_author_name(json_data, 0),
                    'author_name_1': Metadata.get_author_name(json_data, 1),
                    'author_name_2': Metadata.get_author_name(json_data, 2),
                    'ISBN': json_data['message']['ISBN'][2]
                    }

        print('{}: Metadata gathered'.format(doi))
        return metadata

    def get_json_data(self, doi):
        """
        Return json data of doi
        """

        request = requests.get(''.join([self.api_url, doi]))
        return json.loads(request.text)

    @staticmethod
    def get_author_name(json_data, position):
        """
        Returns author name (if any)
        """

        name = ''
        if len(json_data['message']['author']) > position:
            name = '{} {}'\
                   .format(json_data['message']['author'][position]['given'],
                           json_data['message']['author'][position]['family'])
        return name

    @staticmethod
    def write_metadata(metadata, output_file_path):
        """
        Writes metadata to file_name

        TODO add following arguments:
            '-CreationDate={}'
            '-Keywords={ }'
            '-Subject={ }' (abstract)
        """

        arguments = ['-Title={chapter_title}'.format(**metadata),
                     '-Author={}'.format(Metadata
                                         .join_author_names(metadata)),
                     '-Producer={publisher_name}'.format(**metadata),
                     '-ModDate={}'.format(datetime.now()
                                          .strftime("%Y:%m:%d %T"))]

        cmd = ['exiftool']
        cmd.append('-q')
        cmd.extend(arguments)
        cmd.append(output_file_path)

        run(cmd)
        print('{}: Metadata written'
              .format(path.split(output_file_path)[1]))

    @staticmethod
    def join_author_names(metadata):
        """
        Returns a string with author names, separated by semicolon
        """

        metadata_fields = ['author_name_0',
                           'author_name_1',
                           'author_name_2']

        author_names = [metadata[field]
                        for field in metadata_fields
                        if metadata[field]]

        return '; '.join(author_names)
