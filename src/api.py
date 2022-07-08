#!/usr/bin/env python3
from dataclasses import dataclass
from dataclasses import asdict

from os import path
from datetime import datetime
from subprocess import run
from crossref.restful import Works



@dataclass
class Book:
    isbn: str = None
    doi: str = None
    title: str = None
    type: str = None

    @classmethod
    def from_dict(cls, d):
        return Book(**d)


@dataclass
class Chapter:
    author: str = None
    title: str = None
    abstract: str = None
    pages: list[int] = None
    doi: str = None
    licence: str = None
    container_title: str = None
    publisher: str = None

    @classmethod
    def from_dict(cls, d):
        return Chapter(**d)

    @classmethod
    def to_dict(self):
        return asdict(self)


class Metadata:
    '''
    This class retrieve and organise book and chapters metadata
    associated to the user given ISBN.
    '''
    def __init__(self):
        self.works = Works()

    def get_book(self, isbn):
        '''
        Return the book (dataclass) object associated to the supplied ISBN
        '''
        query = self.works.filter(isbn=isbn.replace('-', '')) \
                          .select('title', 'DOI', 'type')
        result = [x for x in query]
        data = {"title": result[0].get("title")[0],
                "doi"  : result[0].get("DOI"),
                "type" : result[0].get("type"),
                "isbn" : isbn}
        return Book(**data)

    def get_chapters(self, book):
        '''
        Returns a python list of chapter dataclasses.
        '''
        query = self.works.filter(container_title=book.title,
                                  type='book-chapter') \
                                  .select('DOI', 'license', 'author',
                                          'title', 'type', 'page',
                                          'publisher', 'container-title',
                                          'abstract')

        # Assert that at least one DOI have been discovered
        if not query:
            raise AssertionError('Couldn\'t find any chapter-level DOIs'
                                 + ' for the supplied --isbn value')

        chapters = []

        for chapter in query:
            data = {"doi"       : chapter.get("DOI"),
                    "author"    : Metadata.join_author_names(chapter),
                    "title"     : chapter.get("title")[0],
                    "publisher" : chapter.get("publisher"),
                    "abstract"  : chapter.get("abstract", ""),
                    "pages"     : chapter.get("page"),
                    "licence"   : Metadata.get_rights(chapter)}

            chapters.append(Chapter(**data))

        return chapters

    def get_doi_suffix(self):
        '''
        Return the book DOI suffix (string)
        '''

        book_types = ['monograph', 'edited-book', 'book']

        book_doi = [item['DOI']
                    for item in self.book_metadata
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

                     '-Author={}'.format(Metadata
                                         .join_author_names(chapter_data)),

                     # Add publisher to the dc:publisher field
                     '-Publisher={}'.format(chapter_data['publisher']),

                     '-ModDate={}'.format(datetime.now()
                                          .strftime("%Y:%m:%d %T")),

                     # Add Abstract in the dc:description field
                     '-Description={}'.format(chapter_data \
                                              .get('abstract', '')),

                     # Add a copyright notice in the dc:rights field
                     '-Copyright={}'.format(Metadata.get_rights(chapter_data)),

                     # Add DOI to the dc:identifier field
                     '-Identifier={}'.format(chapter_data['DOI']),

                     # Add format to the dc:format field
                     '-Format={}'.format('application/pdf'),

                     # Add date to the dc:date field
                     '-Date={}'.format(datetime.now()
                                       .strftime("%Y:%m:%d")),

                     # Add language to the dc:language field
                     '-Language={}'.format('en')]

        cmd = ['exiftool']
        cmd.append('-q')
        cmd.extend(arguments)
        cmd.append(output_file_path)

        run(cmd)
        print('{}: Metadata written'
              .format(path.split(output_file_path)[1]))

    @staticmethod
    def get_rights(chapter_data):
        '''
        Compose a simple copyright statement, just like:
        '© John Doe https://creativecommons.org/licenses/by/2.0/'

        Author name and licence link are pulled out from chapter_data
        '''

        data = {'authors_names': Metadata.join_author_names(chapter_data),
                'copyright_url': chapter_data.get('license', 'n.d.')[0]['URL']}

        rights_str = '© {authors_names} {copyright_url}'.format(**data)

        return rights_str

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
