#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Book:
    isbn: str = None
    doi: str = None

    @classmethod
    def from_dict(cls, d):
        return Book(**d)
