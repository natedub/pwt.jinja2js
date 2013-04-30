(function(__ns, _) {
__ns.trunc = function() {
    var __data = _.parse_args(arguments, ['s']);
    var __output = '';
    __output += _.escape(jinja2filters.string(__data.s));
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
