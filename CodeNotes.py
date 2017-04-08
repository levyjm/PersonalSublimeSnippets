""" CodeNotes is an a Sublime-Text plugin
that allows users to input snippets into a
.json file and retrieve those snippets by
activating the plugin.
"""


import json
import os
import sublime
import sublime_plugin



class AddCommand(sublime_plugin.TextCommand):
    """ This is the a child class of sublime_plugin to
    access the TextCommand's capabilities.
    """


    def run(self, edit, snippet):
        """This is the function invoked when view.run_command('add') is called"""

        self.view.run_command("insert_snippet", {"contents": snippet})

class CodenotesCommand(sublime_plugin.WindowCommand):
    """ This is the default class invoked when
    CodeNotes is selected from the context menu
    """


    def paste_snippet(self, event, snippets):
        """Invokes the AddCommand class"""

        view = self.window.active_view()

        view.run_command('add', {"snippet": snippets[event]})


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

        snippet_names = []
        snippet_values = []


        # PLEASE OPTIMIZE SOON
        for dict in snippets_object["snippets"][lang]:
            for k in dict:
               snippet_names.append(k)

        for dict in snippets_object["snippets"][lang]:
            for v in dict.values():
               snippet_values.append(v)

        self.window.show_quick_panel(snippet_names, lambda event: self.paste_snippet(
            event, snippet_values), 0, 0)

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
        """Parses the name for the snippet to add"""

        name = event

        self.window.show_input_panel("Enter snippet here:",
                                     "",
                                     lambda event: self.add_snippet(
										                               event,    #pylint WTF
                                         lang,
                                         name,
                                         lang_in_set), 0, 0)


    def add_language(self, event, lang_file, lang_in_set):
        """Adds the language file to the languages.txt file"""

        snippet_language = event

        lang_file.write("\n")
        lang_file.write(snippet_language)
        lang_file.close()

        self.window.show_input_panel("Enter a name for your new snippet:",
                                     "", lambda event: self.get_snippet_name(
                                         event, snippet_language, lang_in_set), 0, 0)


    def check_language(self, event, menu_option, lang_set, lang_file):
        """Receives the language and determines if already in set"""

        lang_in_set = True

        if event == (len(lang_set) - 1):
            lang_set.pop(len(lang_set) - 1)
            lang_in_set = False
            self.window.show_input_panel("Add language:",
                                         "", lambda event: self.add_language(
                                             event, lang_file, lang_in_set), 0, 0)
        else:
            snippet_language = lang_set[event]
            if menu_option == 0:
                self.window.show_input_panel("Enter a name for your new snippet:",
                                             "", lambda event: self.get_snippet_name(
                                                 event, snippet_language, lang_in_set), 0, 0)
            elif menu_option == 1:
                self.search_snippet(snippet_language)
                lang_file.close()


    def process_option(self, event):
        """Determines what menu option was selected"""

        try:
            file_path = os.path.dirname(__file__)
            file_name = os.path.join(file_path, 'data_files/languages.txt')
            lang_file = open(file_name, "a+")
            lang_file.seek(0)
            lang_set = list(line.strip() for line in lang_file)
        except (OSError, IOError) as exception:
            print("Could not open, read, or create ",
                  "languages.txt due to error: {0}".format(exception))
            lang_set = set()

        lang_set.append("Add new language")

        menu_option = 0

        if event == 0:
            self.window.show_quick_panel(lang_set, lambda event: self.check_language(
                                             event, menu_option, lang_set, lang_file), 0, 0)
        elif event == 1:
            menu_option = 1
            self.window.show_quick_panel(lang_set, lambda event: self.check_language(
                                             event, menu_option, lang_set, lang_file), 0, 0)


    def run(self):
        """Serves as the main function, kicking things off"""

        global settings
        settings = sublime.load_settings('CodeNotes.sublime-settings')

        menu_options = ["Add new snippet",
                        "Search for snippets",
                       ]

        self.window.show_quick_panel(menu_options, self.process_option, 0, 0)


