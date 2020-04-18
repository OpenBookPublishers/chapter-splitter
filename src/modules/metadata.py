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
    def write_metadata(chapter_data, output_file_path):
        """
        Writes metadata to file_name
        """

        arguments = ['-Title={}'.format(chapter_data['title'][0]),

                     '-Author={}'.format(Metadata \
                                         .join_author_names(chapter_data)),

                     '-Producer={}'.format(chapter_data['publisher']),

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
    def join_author_names(chapter_data):
        """
        Returns a string with author names, separated by semicolon
        """
        # Make a list with author names, i.e. ['Jhon Doe', '']
        authors = [Metadata.get_author_name(chapter_data, 0),
                   Metadata.get_author_name(chapter_data, 1),
                   Metadata.get_author_name(chapter_data, 2)]

        # Return a string with the names, filtering empty fields
        return '; '.join(filter(None, authors))
