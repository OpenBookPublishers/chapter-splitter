#!/usr/bin/env python3

from os import path
import subprocess


def file_checks(file):
    if not path.exists(file):
        raise AssertionError('the path {} doesn\'t exist'.format(file))
    if not path.isfile(file):
        raise AssertionError('the path {} is not a file'.format(file))


def path_checks(folder):
    if not path.exists(folder):
        raise AssertionError('the path {} doesn\'t exist'.format(folder))
    if not path.isdir(folder):
        raise AssertionError('the path {} is not a folder'.format(folder))


def dependencies_checks():
    dependencies = ['exiftool']

    for tool in dependencies:
        if subprocess.call(['which', tool]) != 0:
            raise AssertionError('Tool {} not installed on your system'
                                 .format(tool))
