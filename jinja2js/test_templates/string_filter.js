(function(jinja2js) {
jinja2js.trunc = function() {
    var __data = jinja2support.parse_args(arguments, ['s']);
    var __output = '';
    __output += jinja2support.escape('' + __data.s);
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
