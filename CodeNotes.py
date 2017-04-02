import json
import os
import pprint
import sublime
import sublime_plugin
from . import SnippetInput


""" This is the default class when 
CodeNotes is selected from the context menu
"""
class CodenotesCommand(sublime_plugin.WindowCommand):

	# Add the snippet to current snippets 
	def add_snippet(self, event, lang):
		
		try:
			scriptpath = os.path.dirname(__file__)
			filename = os.path.join(scriptpath, 'data_files/snippets.json')
			snippets_file = open(filename, "a+")
			json.dump(event, snippets_file)
		except (OSError, IOError) as snippet_file_err:
			print("Could not open, read, or create languages.txt" 
				+ " due to error: {0}".format(snippet_file_err))
		


	# Determine what language the snippet is in and process the lang
	def process_language(self, event):

		lang = event

		try:
			scriptpath = os.path.dirname(__file__)
			filename = os.path.join(scriptpath, 'data_files/languages.txt')
			lang_file = open(filename, "a+")
			lang_file.seek(0)
			lang_set = set(line.strip() for line in lang_file)
		except (OSError, IOError) as lang_file_err:
			print("Could not open, read, or create languages.txt due to error: {0}".format(lang_file_err))
			lang_set = set()

		# check in set if language requested is in set and write if not
		if lang not in lang_set:
			lang_file.write(lang)
			lang_file.write("\n")

		lang_file.close()

		self.window.show_input_panel("Enter snippet here:", 
				"", self.add_snippet(event, lang), 0, 0)
	
	# Determine which option to process_option
	def process_option(self, event):
		print(event)

		if event == 0:
			self.window.show_input_panel("Enter snippet language here:", 
				"", self.process_language, 0, 0)
		elif event == 1:
			print("Searching for snippets by name...")
		elif event == 2:
			print("Searching for snippets by language...")
		elif event == 3:
			print("Searching for snippets by snippet...")
	

	# Starts the plugin asking user what to do
	def run(self):

		options = [ "Add new snippet",
					"Search for snippets by name",
					"Search for snippets by language",
					"Search for snippets by snippet" ]

		self.window.show_quick_panel(options, self.process_option, 0, 0)



