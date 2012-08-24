(function(__ns, _) {
__ns.test_obj = function() {
    var __data = _.parse_args(arguments, ['obj']);
    var __output = '';
    __output += _.escape(__data.obj['a']);
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
