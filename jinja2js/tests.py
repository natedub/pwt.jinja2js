import difflib
import fnmatch
import os
import re

from nose.tools import raises

from jinja2 import Environment, PackageLoader
from jinja2.compiler import TemplateAssertionError

import jscompiler


env = Environment(loader=PackageLoader('jinja2js', 'test_templates'),
                  extensions=['jinja2js.ext.Namespace'],
                  autoescape=True)

UPDATE_JS = bool(os.environ.get('UPDATE_JS'))
VERBOSE = bool(os.environ.get('VERBOSE'))
TESTS = os.environ.get('TESTS')
if TESTS:
    TESTS = map(str.strip, TESTS.split(','))

def compare(result, expected):
    # Vim adds an extra linefeed at the end of the file, so we get rid of it
    result = result.strip()
    expected = expected.strip()
    if result != expected:
        if VERBOSE:
            print 'RESULT:'
            print result
            print
            print 'EXPECTED:'
            print expected
            print
            print 'DIFF:'
        for change in difflib.unified_diff(result.strip().split('\n'),
                                           expected.strip().split('\n')):
            print change
        assert False, "Result and expected do not match"

def load_and_compare(source_file, expected_file):
    src = jscompiler.generate(env, expected_file, source_file)
    with open(expected_file, 'w+' if UPDATE_JS else 'r') as f:
        expected = f.read()
        try:
            compare(src, expected)
        except AssertionError:
            if UPDATE_JS:
                f.seek(0)
                f.write(src)
                f.truncate()


def test_file_templates():
    # test will run from either location
    directory = 'jinja2js/test_templates'
    if os.path.isfile('tests.py'):
        directory = 'test_templates'

    files = os.listdir(directory)
    files = fnmatch.filter(files, '*.jinja')

    if TESTS:
        files = [f for f in files if f in TESTS]

    for f in files:
        js_file = os.path.join(directory, re.sub('\\.jinja$', '.js', f))
        yield load_and_compare, f, js_file


@raises(TemplateAssertionError)
def test_undeclared_var():
    # variable is undeclared
    src = """{% macro hello() %}{{ name }}{% endmacro %}"""
    node = env._parse(src, None, None)
    jscompiler._generate(node, env, "var1.html", "var1.html")
