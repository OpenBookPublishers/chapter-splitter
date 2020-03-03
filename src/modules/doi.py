#!/usr/bin/env python3

from .config import Config
from crossref.restful import Works

class Doi:
    def __init__(self, book_level_doi):
        self.book_level_doi = book_level_doi
        self.book_level_doi_suffix = book_level_doi.split('/')[1]

        config = Config()
        self.api_url = config.get_config('metadata', 'api_url')
        self.doi_separator_char = config.get_config('doi',
                                                    'separator_char')
        self.doi_leading_zeros = config.get_config('doi',
                                                   'leading_zeros')

    def discover_ch_dois(self, isbn):
        '''
        Discovers chapter DOIs by quering Crossref agains the
        supplied isbn value. Returns a python list with the
        'chaper level' DOIs.
        '''

        print('Start discovery of chapter-level DOIs')

        works = Works()
        ch_dois = [item['DOI'] \
                   for item in works.filter(isbn=isbn, type='book-chapter')]

        # Assert that at least one DOI have been discovered
        if not ch_dois:
            raise AssertionError('Couln\'t find any chapter-level DOIs'
                                 + ' for the supplied --isbn value')

        return ch_dois
