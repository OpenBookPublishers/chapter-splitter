#!/usr/bin/env python3

import requests
from .config import Config


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

    def discover_ch_dois(self):
        """
        Discovers chapter DOIs by making tentative connections to the
        DOI repository. Successful hits are stored in ch_dois
        """

        ch_dois = []
        print('Start discovery of chapter-level DOIs')

        for counter in range(1, 100):
            doi = ''.join([self.book_level_doi,
                           self.doi_separator_char,
                           str(counter)
                           .zfill(int(self.doi_leading_zeros))])

            try:
                request = requests.head(''.join([self.api_url, doi]))
                request.raise_for_status()

            except requests.exceptions.HTTPError:
                print('Chapter-level DOIs discovery finished.')
                break

            ch_dois.append(doi)
            print('{}: OK'.format(doi))

            # Assert that at least one DOI have been discovered
            if not ch_dois:
                raise AssertionError('Couln\'t find any chapter-level DOIs'
                                     + ' for the supplied --doi value')

        return ch_dois
