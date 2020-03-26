#!/usr/bin/env python3

from crossref.restful import Works

class Doi:
    def __init__(self, isbn):
        self.works = Works()
        self.isbn = isbn

    def get_ch_dois(self):
        '''
        Discovers chapter DOIs by quering Crossref agains the
        supplied isbn value. Returns a python list with the
        'chaper level' DOIs.
        '''

        print('Start discovery of chapter-level DOIs')

        ch_dois = [item['DOI'] \
                   for item in self.works.filter(isbn=self.isbn, \
                                                 type='book-chapter')]

        # Assert that at least one DOI have been discovered
        if not ch_dois:
            raise AssertionError('Couln\'t find any chapter-level DOIs'
                                 + ' for the supplied --isbn value')

        return ch_dois

    def get_doi_suffix(self):
        '''
        Return the book DOI suffix (string)
        '''

        book_types = ['monograph', 'edited-book']

        for book_type in book_types:
            doi = [item['DOI'] \
                   for item in self.works.filter(isbn=self.isbn, \
                                                 type=book_type)]
            if doi:
                break
        else:
            raise AssertionError('Couln\'t find book DOI')

        return doi[0].split('/')[1]
