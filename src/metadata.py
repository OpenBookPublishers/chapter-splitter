#!/usr/bin/env python3
from dataclasses import dataclass, asdict, field
from typing import List

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
    pages: List[int] = field(default_factory=list)
    doi: str = None
    licence: str = None
    publisher: str = None

    @classmethod
    def from_dict(cls, d):
        return Chapter(**d)

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
        return Book.from_dict(data)

    def get_chapters(self, book):
        '''
        Returns a python list of chapter dataclasses.
        '''
        query = self.works.filter(container_title=book.title,
                                  type='book-chapter') \
                                  .select('DOI', 'license', 'author',
                                          'title', 'type', 'page',
                                          'publisher', 'abstract')

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
                    "abstract"  : chapter.get("abstract"),
                    "pages"     : chapter.get("page"),
                    "licence"   : Metadata.get_rights(chapter)}

            chapters.append(Chapter.from_dict(data))

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
    def write_metadata(chapter_dict, output_file_path):
        """
        Writes metadata to file_name
        """
        exiftool_ver = run(["exiftool", "-ver"], capture_output=True, text=True)

        arguments = [f"-Title={chapter_dict.get('title')}",
                     f"-Author={chapter_dict.get('author')}",
                     f"-Publisher={chapter_dict.get('publisher')}",
                     f"-ModDate={datetime.now().strftime('%Y:%m:%d %T')}",
                     f"-Description={chapter_dict.get('abstract', '')}",
                     f"-Copyright={chapter_dict.get('licence')}"
                     f"-Identifier={chapter_dict.get('doi')}",
                      "-Format=application/pdf",
                     f"-CreationDate='{datetime.now().strftime('%Y:%m:%d')}'",
                     f"-Date={datetime.now().strftime('%Y:%m:%d')}",
                     f"-Producer=ExifTool {exiftool_ver.stdout.strip()}",
                      "-Creator=chapter-splitter"]

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
        author_list = []

        for author in chapter_data.get("author"):
            # do not assume we know author's first name
            full_name = [author.get("given", ""), author.get("family", "")]
            author_list.append(" ".join(full_name).strip())

        return '; '.join(author_list)
