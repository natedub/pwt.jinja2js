(function(jinja2js) {
jinja2js.testif = function() {
    var __data = jinja2support.parse_args(arguments, ['option']);
    var __output = '';
    if (__data.option) {
        __output += '\n' + __data.option + '\n';
    }
    __output += '\n';
    return __output;
};

jinja2js.testcall = function() {
    var __data = jinja2support.parse_args(arguments, []);
    var __output = '';
    __output += '\n' + jinja2js.testif(true) + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
