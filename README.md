About
=====

**jinja2js** compiles [Jinja2](http://jinja.pocoo.org/docs/) macros into valid
javascript functions. So you can write your templates once and use them
server and client side.

This version is branched and heavily modified from
[mkerrin/pwt.jinja2ja](https://github.com/mkerrin/pwt.jinja2js), with many
thanks to Michael Kerrin for doing the heavey lifting.

The notable difference with this version is the lack dependencies on external
javascript libraries. A single small javascript support file is included
with the project.

Nutshell
--------

Here a small example of a Jinja template:

    {% macro print_users(users) %}
    <ul>
    {% for user in users %}
        <li><a href="{{ user.url }}">{{ user.username }}</a></li>
    {% endfor %}
    </ul>
    {% endmacro %}


After compiling with jinja2js you get the following:

    __ns.print_users = function() {
        var __data = _.parse_args(arguments, ['users']);
        var __output = '';
        __output += '\n<ul>\n';
        var userList = __data.users;
        var userListLen = userList.length;
        for (var userIndex = 0; userIndex < userListLen; userIndex++) {
            var userData = userList[userIndex];
            __output += '\n    <li><a href="' + _.escape(userData.url) + '">' + _.escape(userData.username) + '</a></li>\n';
        }
        __output += '\n</ul>\n';
        return __output;
    };
    })(window.jinja2js = window.jinja2js || {}, jinja2support);


Usage
=====

The Jinja2 environment is needed to make jinja2js work. Each web framework
has it's own way of accessing the environment, or you can create it yourself.

Here is an example in Flask:

    from flask import current_app
    from jinja2js import jscompiler

    env = current_app.jinja_env

    # name of the template (it doesn't really matter)
    name = "example"

    # relative template path from the templates directory set in the loader
    template = 'example.html'

    # javascript namespace, if not provided the default is 'jinja2js'
    namespace = 'render'

    js_src = jscompiler.generate(loader, env, name, template, namespace)


Example of defining your own Jinja2 environment and loader (taken from `tests.py`):

    from jinja2 import Environment, PackageLoader

    env = Environment(loader=PackageLoader('jinja2js', 'test_templates'))


Testing
=======

To run the tests run

1. Install nose `$ pip install nose`
2. Run the tests `$ nosetests`
