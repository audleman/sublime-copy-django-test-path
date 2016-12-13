import sublime, sublime_plugin
import re


class GenerateTestsClasspathCommand(sublime_plugin.TextCommand):
    """
    Generate, and copy to the clipboard, the text string necessary to run the
    test that your cursor is currently in. Example:

        api.tests.test_model.TestUserProfile.test_foo

    """

    def find_containing_class(self, sel):
        """
        Extract the name of the class above the selection point. Return both
        name and distance from cursor.
        """
        class_defs = self.view.find_all('^class')
        distances = [(sel.a - cd.a, cd) for cd in class_defs]
        distances = [d for d in distances if d[0] >= 0]
        distances = sorted(distances, key=lambda x: x[0])
        closest = distances[0]
        line = self.view.substr(self.view.full_line(closest[1]))
        name = re.search('class (.*?)\(', line).groups(0)[0]
        return name, closest[0]

    def find_containing_function(self, sel):
        """
        Extract name of nearest function above the selection point. Return both
        name and distance from cursor.
        """
        fun_defs = self.view.find_all('^\s*def .*?\(')
        distances = [(sel.a - cd.a, cd) for cd in fun_defs]
        distances = [d for d in distances if d[0] >= 0]
        distances = sorted(distances, key=lambda x: x[0])
        if not distances:
            return None, 999999
        closest = distances[0]
        line = self.view.substr(self.view.full_line(closest[1]))
        name = re.search('def (.*?)\(', line).groups(0)[0]
        return name, closest[0]

    def run(self, edit):
        try:
            # Get filename, concat everything past 'src'
            f_parts = self.view.file_name().replace('.py', '').split('/')
            f_path = '.'.join(f_parts[f_parts.index('src') + 1:])
            # Grab cursor point. Use full line to get to start of line
            sel = self.view.full_line(self.view.sel()[0])
            fun_name, fun_dist = self.find_containing_function(sel)
            class_name, class_dist = self.find_containing_class(sel)
            # Get full line, including trailing newline so we can insert on next
            # line = self.view.full_line(sel)
            # Insert the text
            f_path = '%s.%s' % (f_path, class_name)
            if fun_dist < class_dist and fun_name != 'setUp':
                f_path = '%s.%s' % (f_path, fun_name)
            sublime.set_clipboard(f_path)
            self.view.set_status('key', f_path)
        except:
            self.view.set_status('key', 'something went wrong')
