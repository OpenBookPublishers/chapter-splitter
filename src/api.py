#!/usr/bin/env python3
from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class Book:
    isbn: str = None
    doi: str = None
    chapters: list = None

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
