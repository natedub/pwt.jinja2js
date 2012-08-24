(function(jinja2js) {
jinja2js.test_in = function() {
    var __data = jinja2support.parse_args(arguments, ['name']);
    var __output = '';
    __output += '\n';
    if (jinja2support.in(__data.name, ['bob', 'john'])) {
        __output += 'Yes';
    }
    __output += '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
