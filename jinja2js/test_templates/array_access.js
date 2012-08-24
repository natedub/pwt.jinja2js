(function(jinja2js) {
jinja2js.test_array = function() {
    var __data = jinja2support.parse_args(arguments, ['items']);
    var __output = '';
    __output += __data.items[0];
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
