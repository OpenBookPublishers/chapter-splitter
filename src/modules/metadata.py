#!/usr/bin/env python3

import json
import requests
from os import path
from config import Config
from datetime import datetime
from subprocess import run

class Metadata:
    def __init__(self):
        config = Config()
        self.api_url = config.get_config('metadata', 'api_url')

    def gather_metadata(self, doi):
        ## Returns a dictionary filled with metadata of doi

        json_data = self.get_json_data(doi)

        metadata = {'publisher_name': json_data['message']['publisher'],
                    'licence_url': json_data['message']['license'][0]['URL'],
                    'page_range': json_data['message']['page'].split('-'),
                    'book_title': json_data['message']['container-title'][0],
                    'chapter_title': json_data['message']['title'][0],
                    'author_name_0': self.get_author_name(json_data, 0),
                    'author_name_1': self.get_author_name(json_data, 1),
                    'author_name_2': self.get_author_name(json_data, 2),
                    'ISBN': json_data['message']['ISBN'][2]
        }

        print('{}: Metadata gathered'.format(doi))
        return metadata

    def get_json_data(self, doi):
        ## Return json data of doi

        request = requests.get(''.join([self.api_url, doi]))
        return json.loads(request.text)

    def get_author_name(self, json_data, position):
        ## Returns author name (if any)

        name = ''
        if len(json_data['message']['author']) > position:
            name = '{} {}'\
                   .format(json_data['message']['author'][position]['given'],
                           json_data['message']['author'][position]['family'])
        return name

    def write_metadata(self, metadata, output_file_path):
        ## Writes metadata to file_name

        arguments = ['-Title={chapter_title}'.format(**metadata),
                     '-Author={}'.format(self.join_author_names(metadata)),
                     '-Producer={publisher_name}'.format(**metadata),
                     #~ '-CreationDate={}', ## TODO
                     '-ModDate={}'.format(datetime.now()\
                                               .strftime("%Y:%m:%d %T")),
                     #~ '-Keywords={ }', ## TODO
                     #~ '-Subject={ }', ## TODO (abstract)
        ]

        cmd = ['exiftool']
        cmd.append('-q')
        cmd.extend(arguments)
        cmd.append(output_file_path)

        run(cmd)
        print('{}: Metadata written' \
              .format(path.split(output_file_path)[1]))

    def join_author_names(self, metadata):
        ## Returns a string with author names, separated by semicolon

        metadata_fields = ['author_name_0',
                           'author_name_1',
                           'author_name_2']

        author_names = [metadata[field] \
                        for field in metadata_fields \
                        if metadata[field]]

        return '; '.join(author_names)
