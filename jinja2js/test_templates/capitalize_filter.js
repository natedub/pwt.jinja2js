(function(jinja2js) {
jinja2js.trunc = function() {
    var __data = jinja2support.parse_args(arguments, ['s']);
    var __output = '';
    __output += '\n' + jinja2support.escape(__data.s.substring(0, 1).toUpperCase() + __data.s.substring(1)) + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
