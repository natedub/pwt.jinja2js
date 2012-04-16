import difflib
import unittest

from jinja2 import Environment, PackageLoader

import jinja2.compiler
import jinja2.nodes
import jinja2.optimizer
import jinja2.environment

import jscompiler


def generateMacro(node, environment, name, filename, autoescape=False):
    # Need to test when we are not using an Environment from jinja2js
    generator = jscompiler.MacroCodeGenerator(
        environment, jscompiler.Concat(), None, None)
    eval_ctx = jinja2.nodes.EvalContext(environment, name)
    eval_ctx.autoescape = autoescape
    generator.blockvisit(node.body, jscompiler.JSFrame(environment, eval_ctx))
    return generator.writer.stream.getvalue()


def compare(result, expected):
    if result != expected:
        for change in difflib.unified_diff(result.split('\n'),
                                           expected.split('\n')):
            print change
        assert False, "Result and expected do not match"


class JSConcatCompilerTemplateTestCase(unittest.TestCase):

    def get_compile_from_string(self, source, name=None, filename=None):
        node = self.env._parse(source, name, filename)
        # node = jinja2.optimizer.optimize(node, self.env)

        return node

    def setUp(self):
        super(JSConcatCompilerTemplateTestCase, self).setUp()
        self.env = Environment(loader=PackageLoader('pwt.jinja2js',
                                                    'test_templates'))

    def test_undeclared_var1(self):
        # variable is undeclared
        node = self.get_compile_from_string("""{% macro hello() %}
{{ name }}
{% endmacro %}
""")
        self.assertRaises(
            jinja2.compiler.TemplateAssertionError,
            generateMacro, node, self.env, "var1.html", "var1.html")

    def test_var1(self):
        node = self.get_compile_from_string("""{% macro hello(name) %}
{{ name }}
{% endmacro %}
""")
        source_code = generateMacro(node, self.env, "var1.html", "var1.html")
        expected = """hello = function() {
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
        source_code = generateMacro(node, self.env, "var1.html", "var1.html")
        expected = """hello = function() {
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

        source_code = jscompiler.generate(node, self.env, "f.html", "f.html")

        expected = """forinlist = function() {
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

        source_code = jscompiler.generate(node, self.env, "f.html", "f.html")

        expected = """testif = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {option: arguments[0]};
    var __output = '';
    if (__data.option) {
        __output += __data.option;
    }
    return __output;
};

testcall = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __output = '';
    __output += testif();
    return __output;
};"""
        compare(source_code, expected)

    def test_call_macro3(self):  # Copied from above and modified
        # call macro passing in a argument
        node = self.get_compile_from_string("""{% macro testif(option) -%}
{% if option %}{{ option }}{% endif %}{% endmacro %}

{% macro testcall() %}{{ testif(option=true) }}{% endmacro %}""")

        source_code = jscompiler.generate(node, self.env, "f.html", "f.html")

        expected = """testif = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {option: arguments[0]};
    var __output = '';
    if (__data.option) {
        __output += __data.option;
    }
    return __output;
};

testcall = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __output = '';
    __output += testif(true);
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

        source_code = jscompiler.generate(node, self.env, "cb.html", "cb.html")

        expected = """render_dialog = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {type: arguments[0]};
    var __output = '';
    __output += '<div class="type">' + __caller() + '</div>';
    return __output;
};

render = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {name: arguments[0]};
    var __output = '';
    func_caller = function() {
        var __arg_len = arguments.length;
        var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
        var __output = '';
        __output += 'Hello ' + __data.name + '!';
        return __output;
    };
    __output += render_dialog('box', null, func_caller);
    return __output;
};"""
        compare(source_code, expected)

    def test_filter_capitalize(self):
        # different in concat and stringbuilder modes
        node = self.get_compile_from_string(
            """{% macro trunc(s) %}{{ s|capitalize }}{% endmacro %}""")

        source_code = generateMacro(node, self.env, "f.html", "f.html")

        expected = """trunc = function() {
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

        source_code = generateMacro(node, self.env, "f.html", "f.html")

        expected = """trunc = function() {
    var __arg_len = arguments.length;
    var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;
    var __data = {s: arguments[0]};
    var __output = '';
    __output += '' + __data.s;
    return __output;
};"""

        compare(source_code, expected)
