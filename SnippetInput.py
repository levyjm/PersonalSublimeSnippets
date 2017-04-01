# -*- coding: utf-8 -*-
# @Author: johnlevy
# @Date:   2017-04-01 09:19:35
# @Last Modified by:   johnlevy
# @Last Modified time: 2017-04-01 09:47:16

class Input:

	def __init__(self, language):
		self.languages.append(language)
		self.snippets = []

	def set_code(self, language):
		self.languages.append(language)

	def get_languages(self):
		return self.languages

	def get_codes(self):
		return self.snippets
