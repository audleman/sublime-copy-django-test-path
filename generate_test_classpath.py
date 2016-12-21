import sublime, sublime_plugin
import re
import os


class RunTestsMixin(object):

    def find_project_root(current_directory):
        """
        Start at current directory. Walk up the tree until we find `manage.py`
        """
        MAX_CONFIG_SEARCH_DEPTH = 20
        tries = 0
        while current_directory and tries < MAX_CONFIG_SEARCH_DEPTH:
            potential_path = os.path.join(current_directory, 'manage.py')
            if os.path.exists(potential_path):
                editor_config_file = potential_path
                break

            new_directory = os.path.split(current_directory)[0]
            if current_directory == new_directory:
                break
            current_directory = new_directory
            tries += 1

    def find_containing_class(self, sel):
        """
        Extract the name of the first class above the selection point. Return
        both name and distance from cursor.
        """
        class_defs = self.view.find_all('^class')
        distances = [(sel.a - cd.a, cd) for cd in class_defs]
        distances = [d for d in distances if d[0] >= 0]
        distances = sorted(distances, key=lambda x: x[0])
        if not distances:
            return None, 99999
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

    def run_tests(self, test_path):
        # Launch a SublimeRepl bash shell
        sublime.active_window().run_command(
            "run_existing_window_command",
            {
                "id": "repl_shell",
                "file": "config/Shell/Main.sublime-menu"
            }
        )
        # Run the tests in our shell tab. It was tricky to figure out how to
        # properly pass commands and have them be immediately evaluated
        cmds = [
            'cd ~/robot/malta/',
            'source venv/bin/activate',
            'python manage.py test %s' % test_path]
        sublime.active_window().run_command(
            'repl_send', {
                "external_id": "shell",
                "text": '\n'.join(cmds)})


class RunTestsFileCommand(RunTestsMixin, sublime_plugin.TextCommand):
    """
    Runs tests based on the position of the cursor. Will run one of the
    following, based on the position of the cursor

        - an individual test, if in a function named `test_`
        - a test class, if in a class starting with `Test`
        - a test file, if file has `test_` in its name
        - the module otherwise
    """

    def get_path(self):
        """
        Gets the path of the currently selected file, then drills down and
        tries to get a test class, test method.
        """
        # Get filename, concat everything past 'src'
        file_path = self.view.file_name().replace('.py', '').split('/')
        file_path = file_path[file_path.index('src') + 1:]
        in_test_file = 'test' in file_path[-1]
        if not in_test_file:
            f_path = '.'.join(file_path[:-1])
        else:
            f_path = '.'.join(file_path)
            # Grab cursor point. Use full line to get to start of line
            sel = self.view.full_line(self.view.sel()[0])
            fun_name, fun_dist = self.find_containing_function(sel)
            class_name, class_dist = self.find_containing_class(sel)
            # Add class name if it has Test in it
            if class_name and 'Test' in class_name:
                f_path = '%s.%s' % (f_path, class_name)
            # Add function name if it's test_*
            if fun_dist < class_dist and fun_name.startswith('test'):
                f_path = '%s.%s' % (f_path, fun_name)
        return f_path

    def run(self, edit, action):
        print 'Action is %s' % action
        path = self.get_path()
        self.view.set_status('a_gtp', '')
        sublime.set_clipboard(path)
        self.view.set_status('a_gtp', path)
        if action == 'run':
            self.run_tests(path)


class RunTestsFolderCommand(RunTestsMixin, sublime_plugin.WindowCommand):
    """
    This class gets called when a user right clicks on a file/folder in the
    sidebar. We are passed the path and don't need to check the contents for
    class name / file name like above.
    """

    def get_path(self, paths):
        path = paths[0]
        file_path = path.split('/')
        last = file_path[-1]
        if '.py' in last:
            if 'test_' in last:
                file_path = file_path[:-1] + [last.replace('.py', '')]
            else:
                file_path = file_path[:-1]
        file_path = file_path[file_path.index('src') + 1:]
        file_path = '.'.join(file_path)
        return file_path

    def run(self, paths, action):
        path = self.get_path(paths)
        sublime.set_clipboard(path)
        if action == 'run':
            self.run_tests(path)
        super(RunTestsFolderCommand, self).run()

