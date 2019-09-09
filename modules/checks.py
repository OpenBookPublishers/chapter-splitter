#!/usr/bin/env python3

from os import path
import subprocess

def path_checks(folder):
    assert path.exists(folder), \
           'the path {} doesn\'t exist'.format(folder)
    assert path.isdir(folder), \
           'the path {} is not a folder'.format(folder)

def dependencies_checks():
    dependencies = ['pdfunite', 'exiftool']

    for tool in dependencies:
        test = subprocess.call(['which', tool])

        assert test == 0, \
               'Tool {} not installed on your system'.format(tool)
