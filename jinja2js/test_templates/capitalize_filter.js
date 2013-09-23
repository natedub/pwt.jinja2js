(function(__ns, _) {
var __this = {};
__this.trunc = function() {
    var __data = _.parse_args(arguments, ['s'], []);
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.capitalize(__data.s)) + '\n';
    return __output;
};
__ns['capitalize_filter'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
