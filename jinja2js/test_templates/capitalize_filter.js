(function(__ns, _) {
__ns.trunc = function() {
    var __data = _.parse_args(arguments, ['s'], []);
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.capitalize(__data.s)) + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
