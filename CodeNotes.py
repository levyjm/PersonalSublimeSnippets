""" CodeNotes is an a Sublime-Text plugin
that allows users to input snippets into a
.json file and retrieve those snippets by
activating the plugin.
"""


import json
import os
import sublime
import sublime_plugin



class CodenotesCommand(sublime_plugin.WindowCommand):
    """ This is the default class invoked when
    CodeNotes is selected from the context menu
    """

    def paste_snippet(self, event):
        """Pastes the selected snippet into the user's editor"""
        pass    # Placeholder


    def search_snippet(self, lang):
        """Shows a quick panel displaying the user's snippets
        that he or she selects from"""

        try:
            file_path = os.path.dirname(__file__)
            file_name = os.path.join(file_path, 'data_files/snippets.json')
            snippets_file = open(file_name, "r+")
            snippets_file.seek(0)
        except (OSError, IOError) as exception:
            print("Could not open, read, or create snippets.json"
                  + " due to error: {0}".format(exception))

        snippets_object = json.load(snippets_file)

        snippets = list(set().union(*(dict.keys() for
                                      dict in snippets_object["snippets"][lang])))

        self.window.show_quick_panel(snippets, self.paste_snippet, 0, 0)

    @classmethod
    def add_snippet(cls, event, lang, name, lang_in_set):
        """Adds snippet to the list of current snippets"""

        new_snippet = {name: event}

        # Attempt to open the snippets.json file
        try:
            file_path = os.path.dirname(__file__)
            file_name = os.path.join(file_path, 'data_files/snippets.json')
            snippets_file = open(file_name, "r+")
            snippets_file.seek(0)
        except (OSError, IOError) as exception:
            print("Could not open, read, or create snippets.json"
                  + " due to error: {0}".format(exception))

        # Check to see if the language is already present in json file
        if lang_in_set:
            snippets_object = json.load(snippets_file)
        else:
            snippets_object = json.load(snippets_file)
            snippets_object["snippets"][lang] = []

        snippets_object["snippets"][lang].append(new_snippet)

        # Output new json object to json file
        with snippets_file:
            snippets_file.seek(0)
            snippets_file.write(json.dumps(snippets_object, indent=4))
            snippets_file.truncate()

        snippets_file.close()


    def get_snippet_name(self, event, lang, lang_in_set):
        """Parses the name given by the user for the snippet's identifier"""
        name = event

        self.window.show_input_panel("Enter snippet here:",
                                     "",
                                     lambda event: self.add_snippet(
										                               event,    #pylint WTF
                                         lang,
                                         name,
                                         lang_in_set), 0, 0)


    def check_language(self, event, option):
        """Receives the language and determines if already in set"""

        process_option = option

        lang_in_set = True

        snippet_language = event

        # Attempt to open the languages.txt file
        try:
            file_path = os.path.dirname(__file__)
            file_name = os.path.join(file_path, 'data_files/languages.txt')
            lang_file = open(file_name, "a+")
            lang_file.seek(0)
            lang_set = set(line.strip() for line in lang_file)
        except (OSError, IOError) as exception:
            print("Could not open, read, or create ",
                  "languages.txt due to error: {0}".format(exception))
            lang_set = set()

        # check in set if language requested is in set and write if not
        if snippet_language not in lang_set:
            lang_file.write(snippet_language)
            lang_file.write("\n")
            lang_in_set = False

        lang_file.close()

        if process_option == 0:
            self.window.show_input_panel("Enter a name for your new snippet:",
                                         "", lambda event: self.get_snippet_name(
                                             event, snippet_language, lang_in_set), 0, 0)
        elif process_option == 1:
            self.search_snippet(snippet_language)


    def process_option(self, event):
        """Determines what menu option was selected"""

        menu_option = 0

        print(event)

        if event == 0:
            self.window.show_input_panel("Enter snippet language here:",
                                         "", lambda event: self.check_language(
                                             event, menu_option), 0, 0)
        elif event == 1:
            menu_option = 1
            self.window.show_input_panel("Find your snippets for ",
                                         "which language?",
                                         "", lambda event: self.check_language(
                                             event, menu_option), 0, 0)


    def run(self):
        """Serves as the main function, kicking things off"""
        menu_options = ["Add new snippet",
                        "Search for snippets",
                       ]

        self.window.show_quick_panel(menu_options, self.process_option, 0, 0)


