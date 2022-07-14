#!/usr/bin/env python3
from dataclasses import dataclass, asdict
from typing import List, Dict

from os import path
from datetime import datetime
from subprocess import run

from db import Crossref, Thoth


@dataclass
class Book:
    doi: str = None
    title: str = None

    @classmethod
    def from_dict(cls, d):
        return Book(**d)

    def to_dict(self):
        return asdict(self)


@dataclass
class Chapter:
    author: str = None
    title: str = None
    abstract: str = None
    pages: str = None
    doi: str = None
    licence: str = None
    publisher: str = None

    @classmethod
    def from_dict(cls, d):
        return Chapter(**d)

    def to_dict(self):
        return asdict(self)


class Metadata:
    """Class retrieve and organise book and chapters metadata

    Data is retrieved from a selected source (database) and the result is
    stored in Book and Chapter objects. These objects live inside this class:
    every time data is sent to other modules is converted into a dictionary
    representation. Same applies when data in fetched.
    """

    def __init__(self, database="thoth", doi=None):
        if database == "thoth":
            self.db = Thoth(doi)
        if database == "crossref":
            self.db = Crossref(doi)

        self.book = self.fetch_book_data()
        self.chapters = self.fetch_chapter_data()

    def fetch_book_data(self) -> Book:
        """Query DB and return book data in a Book object"""
        return Book.from_dict(self.db.get_book())

    def fetch_chapter_data(self) -> List[Chapter]:
        """Query DB and return a list of chapter data as Chapter objects"""
        return [Chapter.from_dict(chapter) for chapter
                in self.db.get_chapters(self.book.to_dict())]

    def get_chapters(self) -> List[Dict]:
        """Return a list of Chapters (dictionaries)"""
        return [chapter.to_dict() for chapter in self.chapters]

    @staticmethod
    def write_metadata(chapter_dict, output_file_path):
        """Writes metadata to file_name"""

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
        """Compose a simple copyright statement

        This method return a copyright statement which looks like:
        '© John Doe https://creativecommons.org/licenses/by/2.0/'
        """

        data = {'authors_names': chapter_data.get('author'),
                'copyright_url': chapter_data.get('licence')}

        rights_str = '© {authors_names} {copyright_url}'.format(**data)

        return rights_str
