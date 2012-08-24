(function(jinja2js) {
jinja2js.array_slice = function() {
    var __data = jinja2support.parse_args(arguments, ['arr']);
    var __output = '';
    __output += jinja2support.escape(__data.arr.slice(0, 4));
    return __output;
};

jinja2js.array_slice_no_start = function() {
    var __data = jinja2support.parse_args(arguments, ['arr']);
    var __output = '';
    __output += jinja2support.escape(__data.arr.slice(0, 4));
    return __output;
};

jinja2js.array_slice_no_end = function() {
    var __data = jinja2support.parse_args(arguments, ['arr']);
    var __output = '';
    __output += jinja2support.escape(__data.arr.slice(1));
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
