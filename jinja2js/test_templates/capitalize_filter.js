(function(__ns, _) {
__ns.trunc = function() {
    var __data = _.parse_args(arguments, ['s']);
    var __output = '';
    __output += '\n' + _.escape(__data.s.substring(0, 1).toUpperCase() + __data.s.substring(1)) + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
