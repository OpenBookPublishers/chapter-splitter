#!/usr/bin/env python3
from dataclasses import dataclass, asdict, field
from typing import List

from os import path
from datetime import datetime
from subprocess import run

from db import Crossref


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
    def __init__(self, database="crossref"):
        if database == "crossref":
            self.db = Crossref()

    def get_book(self, isbn):
        '''
        Return the book (dataclass) object associated to the supplied ISBN
        '''
        data = self.db.get_book(isbn)
        return Book.from_dict(data)

    def get_chapters(self, book):
        '''
        Returns a python list of chapter dataclasses.
        '''
        chapters = [Chapter.from_dict(chapter) for chapter
                    in self.db.get_chapters(book)]
        return chapters

    @staticmethod
    def write_metadata(chapter_dict, output_file_path):
        """
        Writes metadata to file_name
        """

        arguments = [f"-Title={chapter_dict.get('title')}",
                     f"-Author={chapter_dict.get('author')}",
                     f"-Publisher={chapter_dict.get('publisher')}",
                     f"-ModDate={datetime.now().strftime('%Y:%m:%d %T')}",
                     f"-Description={chapter_dict.get('abstract', '')}",
                     f"-Copyright={Metadata.get_rights(chapter_dict)}",
                     f"-Identifier={chapter_dict.get('doi')}",
                     "-Format=application/pdf",
                     f"-CreationDate='{datetime.now().strftime('%Y:%m:%d')}'",
                     f"-Date={datetime.now().strftime('%Y:%m:%d')}",
                     f"-Producer=PyMuPDF",
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

        data = {'authors_names': chapter_data.get('author'),
                'copyright_url': chapter_data.get('licence')}

        rights_str = '© {authors_names} {copyright_url}'.format(**data)

        return rights_str
