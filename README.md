# What is this?

I often run individual tests or just one test class in my Django project. I got
tired of figuring out and hand typing the path, so I wrote this plugin to figure
out what it is and copy it to the clipboard for me.


## Installation instructions

1. Install SublimeREPL
2. Install this package

### Install SublimeREPL

Use `Package Control: Install Package`

### Install this package

Clone the repo in your Plugins folder. For OSX:

```
git clone git@github.com:audleman/sublime-copy-django-test-path.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/CopyDjangoTestPath
```

## How to use

Let's say you have the file
```
my_app/tests/test_model.py
```

and inside is 

```
class TestMyModel(TestCase):

    def test_foo(self):
        pass
```

Simply right click when inside a test and chose `Run tests`.

If you do this at the top of the class it will generate the string to run the
whole test class.

If you do it outside of a test class it will probably throw an exception and
silently do nothing.

Need to explain all entry points. More exist, such as right clicking on a
file/folder in the side bar
