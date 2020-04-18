#!/usr/bin/env python3

from os import path
from datetime import datetime
from subprocess import run
from crossref.restful import Works


class Metadata:
    '''
    This class retrieve and organise book and chapters metadata
    associated to the user given ISBN.
    '''
    def __init__(self, isbn):
        self.works = Works()
        self.isbn = isbn

        # Get book metadata
        self.book_metadata = self.get_book_metadata()

    def get_book_metadata(self):
        '''
        Get book metadata, which include all the entries
        associated to the supplied ISBN
        (i.e. type: book, book-chapter)
        '''
        return self.works.filter(isbn=self.isbn) \
                         .select('DOI', 'license', 'author',
                                 'title', 'type', 'page',
                                 'publisher', 'container-title')

    def get_chapters_data(self):
        '''
        Returns a python list of dictionaries with the book chapter data.

        This task is made inexpensive by filtering the broader data set
        contained in self.book_metadata
        '''
        chapters_data = [item for item in self.book_metadata \
                         if item['type'] == 'book-chapter']

        # Assert that at least one DOI have been discovered
        if not chapters_data:
            raise AssertionError('Couldn\'t find any chapter-level DOIs'
                                 + ' for the supplied --isbn value')

        return chapters_data

    def get_doi_suffix(self):
        '''
        Return the book DOI suffix (string)
        '''

        book_types = ['monograph', 'edited-book', 'book']

        book_doi = [item['DOI'] \
                    for item in self.book_metadata \
                    if item['type'] in book_types]

        if not book_doi:
            raise AssertionError('Couldn\'t find book DOI')

        return book_doi[0].split('/')[1]

    def gather_work_data(self, chapter_data):
        """
        Get raw chapter_data and return a dictionary of chapter 
        metadata in a form which is easier to work with.
        """

        metadata = {'publisher_name': chapter_data['publisher'],
                    'licence_url': chapter_data['license'][0]['URL'],
                    'page_range': chapter_data['page'].split('-'),
                    'book_title': chapter_data['container-title'][0],
                    'chapter_title': chapter_data['title'][0],
                    'author_name_0': self.get_author_name(chapter_data, 0),
                    'author_name_1': self.get_author_name(chapter_data, 1),
                    'author_name_2': self.get_author_name(chapter_data, 2),
                    'DOI': chapter_data['DOI']
        }

        print('{}: Metadata gathered'.format(metadata['DOI']))
        return metadata

    @staticmethod
    def get_author_name(data, position):
        """
        Returns author name (if specified for the given position)
        """

        name = ''
        if len(data['author']) > position:
            name = '{} {}'\
                   .format(data['author'][position]['given'],
                           data['author'][position]['family'])
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
