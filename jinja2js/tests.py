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


def compare(result, expected):
    # Vim adds an extra linefeed at the end of the file, so we get rid of it
    result = result.strip()
    expected = expected.strip()
    if result != expected:
        for change in difflib.unified_diff(result.strip().split('\n'),
                                           expected.strip().split('\n')):
            print change
        assert False, "Result and expected do not match"


def load_and_compare(source_file, expected_file):
    src = jscompiler.generate(env, expected_file, source_file)
    with open(expected_file) as f:
        expected = f.read()
        compare(src, expected)


def test_file_templates():
    # test will run from either location
    directory = 'jinja2js/test_templates'
    if os.path.isfile('tests.py'):
        directory = 'test_templates'

    files = os.listdir(directory)
    files = fnmatch.filter(files, '*.jinja')

    for f in files:
        js_file = os.path.join(directory, re.sub('\\.jinja$', '.js', f))
        yield load_and_compare, f, js_file


@raises(TemplateAssertionError)
def test_undeclared_var():
    # variable is undeclared
    src = """{% macro hello() %}{{ name }}{% endmacro %}"""
    node = env._parse(src, None, None)
    jscompiler._generate(node, env, "var1.html", "var1.html")
