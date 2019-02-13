#!/usr/bin/env python3

from os import path
import configparser

class Config:
	def __init__(self):
		# Get config file absolute path
		modules_path = path.dirname(path.realpath(__file__))
		project_path = path.split(modules_path)[0]
		self.config_file_path = (path.join(project_path, 'config.ini'))

		self.config = configparser.ConfigParser()
		self.config.read(self.config_file_path)

	def get_config(self, section, item):
		return self.config.get(section, item)
