(function(jinja2js) {
jinja2js.test_obj = function() {
    var __data = jinja2support.parse_args(arguments, ['obj']);
    var __output = '';
    __output += __data.obj['a'];
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
