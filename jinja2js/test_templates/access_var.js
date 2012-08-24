(function(__ns, _) {
__ns.hello = function() {
    var __data = _.parse_args(arguments, ['name']);
    var __output = '';
    __output += '\n' + _.escape(__data.name) + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
