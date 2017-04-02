import json
import pprint
import sublime
import sublime_plugin
from . import SnippetInput


# Default class when CodeNotes is selected from the context menu
class CodenotesCommand(sublime_plugin.WindowCommand):

	# Add the snippet to current snippets 
	def add_snippet(self, event):
		scriptpath = os.path.dirname(__file__)
		filename = os.path.join(scriptpath, 'data_files/snippets.json')
		snippets_file = open(filename, "w+")

		json.dump(event, snippets_file)


	# Determine what language the snippet is in and process the lang
	def process_language(self, event):

		# Get list of languages
		scriptpath = os.path.dirname(__file__)

		try:
			filename = os.path.join(scriptpath, 'data_files/languages.txt')
			lang_file = open(filename, "a+")
			lang_set = set(lang_file.readlines())
		except (OSError, IOError) as err:
			print("Could not open, read, or create file due to error: {0}".format(err))

		# check in set if language requested is in set and write if not
		if not event in lang_set:
			lang_file.write(event)
			lang_file.write("\n")

		lang_file.close()

		self.window.show_input_panel("Enter snippet here:", 
				"", self.add_snippet, 0, 0)
	
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



