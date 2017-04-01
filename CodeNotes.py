import json
import pprint
import sublime
import sublime_plugin
from . import snippet_input


# Default class when CodeNotes is selected from the context menu
class CodenotesCommand(sublime_plugin.WindowCommand):

	#def add_snippet(self, event):

	# Determine what language the snippet is in and process the lang
	def process_language(self, event):

		# Get list of languages
		scriptpath = os.path.dirname(__file__)
		filename = os.path.join(scriptpath, 'languages.txt')
		lang_file = open(filename, "r+")
		lang_set = set(lang_file.readlines())

		# check in set if language requested is in set and write if not
		if not event in lang_set:
			lang_file.write(event)
			lang_file.write("\n")
			
		lang_file.close()


		scriptpath = os.path.dirname(__file__)
		filename = os.path.join(scriptpath, 'snippets.json')
		snippets_file = open(filename, "w+")

		json.dump(event, snippets_file)
	
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



