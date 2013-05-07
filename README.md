About
=====

**jinja2js** compiles [Jinja2](http://jinja.pocoo.org/docs/) macros into valid
javascript functions. So you can write your templates once and use them
server and client side.

This version is branched and heavily modified from
[mkerrin/pwt.jinja2ja](https://github.com/mkerrin/pwt.jinja2js), with many
thanks to Michael Kerrin for doing the heavey lifting.

### The notable difference with this version:

- Lack dependencies on external javascript libraries
- A single small javascript support file is included with the project
- Full support for key word arguments
- Python compatible boolean equivalents, such as empty list, objects and
  zeros treated as `False`.

Nutshell
--------

Here a small example of a Jinja template:

    {% macro print_users(users, show_names=False) %}
    <ul>
    {% for user in users %}
        <li>
        {% if show_names %}{{ user.name }}: {% endif %}
        <a href="{{ user.url }}">{{ user.username }}</a></li>
    {% endfor %}
    </ul>
    {% endmacro %}


After compiling with jinja2js you get the following:

    (function(__ns, _) {

    __ns.print_users = function() {
        var __data = _.parse_args(arguments, ['users'], [['show_names', false]]);
        var __output = '';
        __output += '\n<ul>\n';
        var userList = __data.users;
        var userListLen = userList.length;
        for (var userIndex = 0; userIndex < userListLen; userIndex++) {
            var userData = userList[userIndex];
            __output += '\n    <li>\n    ';
            if (_.truth(__data.show_names)) {
                __output += userData.name + ': ';
            }
            __output += '\n    <a href="' + userData.url + '">' + userData.username + '</a></li>\n';
        }
        __output += '\n</ul>\n';
        return __output;
    };
    })(this.jinja2js = this.jinja2js || {}, jinja2support);

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
