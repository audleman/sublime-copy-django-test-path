# What is this?

I often run individual tests or just one test class in my Django project. I got
tired of figuring out and hand typing the path, so I wrote this plugin to figure
out what it is and copy it to the clipboard for me.


## Installation instructions

Clone the repo in your Plugins folder. For OSX:

```
git clone git@github.com:audleman/sublime-copy-django-test-path.git ~/Library/Application Support/Sublime Text 2/Packages $ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/CopyDjangoTestPath
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

Simply right click when inside a test and chose `Copy Django Test Path`. Go 
to your shell and Ctrl+v

If you do this at the top of the class it will generate the string to run the
whole test class.

If you do it outside of a test class it will probably throw an exception and
silently do nothing.

The path copied is displayed in the status bar.
