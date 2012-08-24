(function(jinja2js) {
jinja2js.test_array_dot = function() {
    var __data = jinja2support.parse_args(arguments, ['items']);
    var __output = '';
    __output += '\n' + __data.items.large[0].name + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
