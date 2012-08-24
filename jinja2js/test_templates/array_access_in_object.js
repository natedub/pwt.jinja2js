(function(__ns, _) {
__ns.test_array_dot = function() {
    var __data = _.parse_args(arguments, ['items']);
    var __output = '';
    __output += '\n' + _.escape(__data.items.large[0].name) + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
