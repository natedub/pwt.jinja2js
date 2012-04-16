import difflib
import unittest

from jinja2 import Environment, PackageLoader

import jinja2.compiler
import jinja2.nodes
import jinja2.optimizer
import jinja2.environment

import jscompiler


env = Environment(loader=PackageLoader('pwt.jinja2js', 'test_templates'))


def compare(result, expected):
    if result != expected:
        for change in difflib.unified_diff(result.split('\n'),
                                           expected.split('\n')):
            print change
        assert False, "Result and expected do not match"


class JSConcatCompilerTemplateTestCase(unittest.TestCase):

    def get_compile_from_string(self, source, name=None, filename=None):
        node = env._parse(source, name, filename)
        # node = jinja2.optimizer.optimize(node, env)

        return node

    def setUp(self):
        super(JSConcatCompilerTemplateTestCase, self).setUp()

    def test_undeclared_var1(self):
        # variable is undeclared
        node = self.get_compile_from_string("""{% macro hello() %}
{{ name }}
{% endmacro %}
""")
        self.assertRaises(
            jinja2.compiler.TemplateAssertionError,
            jscompiler.generate, node, env, "var1.html", "var1.html")

    def test_var1(self):
        node = self.get_compile_from_string("""{% macro hello(name) %}
{{ name }}
{% endmacro %}
""")
        source_code = jscompiler.generate(node, env, "var1.html", "var1.html")
        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.hello = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {name: arguments[0]};
    var __output = '';
    __output += '\\n' + __data.name + '\\n';
    return __output;
};"""
        compare(source_code, expected)

    def test_var2(self):
        node = self.get_compile_from_string("""{% macro hello(person) %}
{{ person.name }}
{% endmacro %}
""")
        source_code = jscompiler.generate(node, env, "var1.html", "var1.html")
        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.hello = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {person: arguments[0]};
    var __output = '';
    __output += '\\n' + __data.person.name + '\\n';
    return __output;
};"""
        compare(source_code, expected)

    def test_for13(self):
        # XXX - test for loop for conflicting variables. Here we have a
        # namespaced variable that gets required but conflicts with the
        # variable inside the loop that we created. If this is a problem
        # I will fix it, but it probable won't
        node = self.get_compile_from_string(
        """{% macro forinlist(jobs) -%}
{% for job in jobs %}{{ job.name }} does {{ jobData.name }}{% endfor %}
{%- endmacro %}""")

        source_code = jscompiler.generate(node, env, "f.html", "f.html")

        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.forinlist = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {jobs: arguments[0]};
    var __output = '';
    var jobList = __data.jobs;
    var jobListLen = jobList.length;
    for (var jobIndex = 0; jobIndex < jobListLen; jobIndex++) {
        var jobData = jobList[jobIndex];
        __output += jobData.name + ' does ' + jobData.name;
    }
    return __output;
};"""

        compare(source_code, expected)

    def test_call_macro1(self):
        # call macro in same template, without arguments.
        node = self.get_compile_from_string("""{% macro testif(option) -%}
{% if option %}{{ option }}{% endif %}{% endmacro %}

{% macro testcall() %}{{ testif() }}{% endmacro %}""")

        source_code = jscompiler.generate(node, env, "f.html", "f.html")

        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.testif = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {option: arguments[0]};
    var __output = '';
    if (__data.option) {
        __output += __data.option;
    }
    return __output;
};

jinja2js.testcall = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __output = '';
    __output += jinja2js.testif();
    return __output;
};"""
        compare(source_code, expected)

    def test_call_macro3(self):  # Copied from above and modified
        # call macro passing in a argument
        node = self.get_compile_from_string("""{% macro testif(option) -%}
{% if option %}{{ option }}{% endif %}{% endmacro %}

{% macro testcall() %}{{ testif(option=true) }}{% endmacro %}""")

        source_code = jscompiler.generate(node, env, "f.html", "f.html")

        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.testif = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {option: arguments[0]};
    var __output = '';
    if (__data.option) {
        __output += __data.option;
    }
    return __output;
};

jinja2js.testcall = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __output = '';
    __output += jinja2js.testif(true);
    return __output;
};"""
        compare(source_code, expected)

    def test_callblock1(self):
        node = self.get_compile_from_string("""{% macro render_dialog(type) -%}
<div class="type">{{ caller() }}</div>
{%- endmacro %}

{% macro render(name) -%}
{% call render_dialog(type = 'box') -%}
Hello {{ name }}!
{%- endcall %}
{%- endmacro %}
""")

        source_code = jscompiler.generate(node, env, "cb.html", "cb.html")

        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.render_dialog = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {type: arguments[0]};
    var __output = '';
    __output += '<div class="type">' + __caller() + '</div>';
    return __output;
};

jinja2js.render = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {name: arguments[0]};
    var __output = '';
    func_caller = function() {
        var __output = '';
        __output += 'Hello ' + __data.name + '!';
        return __output;
    };
    __output += jinja2js.render_dialog('box', null, func_caller);
    return __output;
};"""
        compare(source_code, expected)

    def test_filter_capitalize(self):
        # different in concat and stringbuilder modes
        node = self.get_compile_from_string(
            """{% macro trunc(s) %}{{ s|capitalize }}{% endmacro %}""")

        source_code = jscompiler.generate(node, env, "f.html", "f.html")

        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.trunc = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {s: arguments[0]};
    var __output = '';
    __output += __data.s.substring(0, 1).toUpperCase() + __data.s.substring(1);
    return __output;
};"""

        compare(source_code, expected)

    def test_filter_string(self):
        # different in concat and stringbuilder modes
        node = self.get_compile_from_string(
            """{% macro trunc(s) %}{{ s|string }}{% endmacro %}""")

        source_code = jscompiler.generate(node, env, "f.html", "f.html")

        expected = """if(typeof jinja2js == 'undefined') {var jinja2js = {};}

jinja2js.trunc = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {s: arguments[0]};
    var __output = '';
    __output += '' + __data.s;
    return __output;
};"""

        compare(source_code, expected)
