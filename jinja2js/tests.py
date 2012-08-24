import difflib
import unittest

from jinja2 import Environment, PackageLoader

import jinja2.compiler
import jinja2.nodes
import jinja2.optimizer
import jinja2.environment

import jscompiler


env = Environment(loader=PackageLoader('jinja2js', 'test_templates'))


def compare(result, expected):
    if result != expected:
        for change in difflib.unified_diff(result.split('\n'),
                                           expected.split('\n')):
            print change
        assert False, "Result and expected do not match"


def compile_from_string(source, name=None, filename=None):
    node = env._parse(source, name, filename)
    # node = jinja2.optimizer.optimize(node, env)

    return node


def compile_and_compare(source, expected):
    node = compile_from_string(source)
    compiled = jscompiler._generate(node, env, None, None, 'jinja2js')
    compare(compiled, expected)


class JSCompilerTemplateTestCase(unittest.TestCase):

    def test_undeclared_var1(self):
        # variable is undeclared
        node = compile_from_string("{% macro hello() %}{{ name }}"
                                   "{% endmacro %} ")
        self.assertRaises(jinja2.compiler.TemplateAssertionError,
                          jscompiler._generate, node, env, "var1.html",
                          "var1.html", 'jinja2js')

    def test_var1(self):
        source = """{% macro hello(name) %}
{{ name }}
{% endmacro %}
"""
        expected = """(function(jinja2js) {
jinja2js.hello = function() {
    var __data = jinja2support.parse_args(arguments, ['name']);
    var __output = '';
    __output += '\\n' + __data.name + '\\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""
        compile_and_compare(source, expected)

    def test_var2(self):
        source = """{% macro hello(person) %}
{{ person.name }}
{% endmacro %}
"""
        expected = """(function(jinja2js) {
jinja2js.hello = function() {
    var __data = jinja2support.parse_args(arguments, ['person']);
    var __output = '';
    __output += '\\n' + __data.person.name + '\\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""
        compile_and_compare(source, expected)

    def test_in_operand(self):
        source = """{% macro test_in(name) %}
{% if name in ['bob', 'john'] %}Yes{% endif %}
{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.test_in = function() {
    var __data = jinja2support.parse_args(arguments, ['name']);
    var __output = '';
    __output += '\\n';
    if (jinja2support.in(__data.name, ['bob', 'john'])) {
        __output += 'Yes';
    }
    __output += '\\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""
        compile_and_compare(source, expected)

    def test_not_in_operand(self):
        source = """{% macro test_not_in(name) %}
{% if name not in ['bob', 'john'] %}No{% endif %}
{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.test_not_in = function() {
    var __data = jinja2support.parse_args(arguments, ['name']);
    var __output = '';
    __output += '\\n';
    if (!jinja2support.in(__data.name, ['bob', 'john'])) {
        __output += 'No';
    }
    __output += '\\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""
        compile_and_compare(source, expected)

    def test_for13(self):
        # XXX - test for loop for conflicting variables. Here we have a
        # namespaced variable that gets required but conflicts with the
        # variable inside the loop that we created. If this is a problem
        # I will fix it, but it probable won't
        source = """{% macro forinlist(jobs) -%}
{% for job in jobs %}{{ job.name }} does {{ jobData.name }}{% endfor %}
{%- endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.forinlist = function() {
    var __data = jinja2support.parse_args(arguments, ['jobs']);
    var __output = '';
    var jobList = __data.jobs;
    var jobListLen = jobList.length;
    for (var jobIndex = 0; jobIndex < jobListLen; jobIndex++) {
        var jobData = jobList[jobIndex];
        __output += jobData.name + ' does ' + jobData.name;
    }
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""

        compile_and_compare(source, expected)

    def test_call_macro1(self):
        # call macro in same template, without arguments.
        source = """{% macro testif(option) -%}
{% if option %}{{ option }}{% endif %}{% endmacro %}

{% macro testcall() %}{{ testif() }}{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.testif = function() {
    var __data = jinja2support.parse_args(arguments, ['option']);
    var __output = '';
    if (__data.option) {
        __output += __data.option;
    }
    return __output;
};

jinja2js.testcall = function() {
    var __data = jinja2support.parse_args(arguments, []);
    var __output = '';
    __output += jinja2js.testif();
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""
        compile_and_compare(source, expected)

    def test_call_macro3(self):  # Copied from above and modified
        # call macro passing in a argument
        source = """{% macro testif(option) -%}
{% if option %}{{ option }}{% endif %}{% endmacro %}

{% macro testcall() %}{{ testif(option=true) }}{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.testif = function() {
    var __data = jinja2support.parse_args(arguments, ['option']);
    var __output = '';
    if (__data.option) {
        __output += __data.option;
    }
    return __output;
};

jinja2js.testcall = function() {
    var __data = jinja2support.parse_args(arguments, []);
    var __output = '';
    __output += jinja2js.testif(true);
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""
        compile_and_compare(source, expected)

    def test_callblock1(self):
        source = """{% macro render_dialog(type) -%}
<div class="type">{{ caller() }}</div>
{%- endmacro %}

{% macro render(name) -%}
{% call render_dialog(type = 'box') -%}
Hello {{ name }}!
{%- endcall %}
{%- endmacro %}
"""

        expected = """(function(jinja2js) {
jinja2js.render_dialog = function() {
    var __data = jinja2support.parse_args(arguments, ['type']);
    var __output = '';
    __output += '<div class="type">' + __data.__caller() + '</div>';
    return __output;
};

jinja2js.render = function() {
    var __data = jinja2support.parse_args(arguments, ['name']);
    var __output = '';
    func_caller = function() {
        var __output = '';
        __output += 'Hello ' + __data.name + '!';
        return __output;
    };
    __output += jinja2js.render_dialog('box', null, func_caller);
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""
        compile_and_compare(source, expected)

    def test_filter_capitalize(self):
        # different in concat and stringbuilder modes
        source = """{% macro trunc(s) %}{{ s|capitalize }}{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.trunc = function() {
    var __data = jinja2support.parse_args(arguments, ['s']);
    var __output = '';
    __output += __data.s.substring(0, 1).toUpperCase() + __data.s.substring(1);
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""

        compile_and_compare(source, expected)

    def test_filter_string(self):
        # different in concat and stringbuilder modes
        source = """{% macro trunc(s) %}{{ s|string }}{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.trunc = function() {
    var __data = jinja2support.parse_args(arguments, ['s']);
    var __output = '';
    __output += '' + __data.s;
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""

        compile_and_compare(source, expected)

    def test_dotted_array_name(self):
        source = """{% macro test_array_dot(items) %}
{{items.large[0].name}}
{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.test_array_dot = function() {
    var __data = jinja2support.parse_args(arguments, ['items']);
    var __output = '';
    __output += '\\n' + __data.items.large[0].name + '\\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""

        compile_and_compare(source, expected)

    def test_array_value(self):
        source = """{% macro test_array(items) %}{{items[0]}}{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.test_array = function() {
    var __data = jinja2support.parse_args(arguments, ['items']);
    var __output = '';
    __output += __data.items[0];
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""

        compile_and_compare(source, expected)

    def test_object_value(self):
        source = """{% macro test_obj(obj) %}{{obj['a']}}{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.test_obj = function() {
    var __data = jinja2support.parse_args(arguments, ['obj']);
    var __output = '';
    __output += __data.obj['a'];
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""

        compile_and_compare(source, expected)

    def test_object_value_double_quote(self):
        source = """{% macro test_obj(obj) %}{{obj["a"]}}{% endmacro %}"""

        expected = """(function(jinja2js) {
jinja2js.test_obj = function() {
    var __data = jinja2support.parse_args(arguments, ['obj']);
    var __output = '';
    __output += __data.obj['a'];
    return __output;
};
})(window.jinja2js = window.jinja2js || {});"""

        compile_and_compare(source, expected)
