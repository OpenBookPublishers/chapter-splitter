#!/usr/bin/env python3

from crossref.restful import Works

class Doi:
    def __init__(self, isbn):
        self.works = Works()
        self.isbn = isbn
        self.book_metadata = self.get_book_metadata()

    def get_book_metadata(self):
        '''
        Get book metadata, which include all the entries
        associated to the supplied ISBN
        (i.e. type: book, book-chapter)
        '''

        return self.works.filter(isbn=self.isbn) \
                         .select('DOI', 'license', 'author',
                                 'title', 'type', 'page')

    def get_ch_dois(self):
        '''
        Discovers chapter DOIs by querying Crossref against the
        supplied ISBN value. Returns a python list with the
        'chapter level' DOIs.
        '''

        print('Start discovery of chapter-level DOIs')

        ch_dois = [item['DOI'] \
                   for item in self.book_metadata \
                   if item['type'] == 'book-chapter']

        # Assert that at least one DOI have been discovered
        if not ch_dois:
            raise AssertionError('Couldn\'t find any chapter-level DOIs'
                                 + ' for the supplied --isbn value')

        return ch_dois

    def get_doi_suffix(self):
        '''
        Return the book DOI suffix (string)
        '''

        book_types = ['monograph', 'edited-book']

        book_doi = [item['DOI'] \
                    for item in self.book_metadata \
                    if item['type'] in book_types]

        if not book_doi:
            raise AssertionError('Couldn\'t find book DOI')

        return book_doi[0].split('/')[1]
