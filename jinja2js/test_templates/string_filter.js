(function(__ns, _) {
var __this = {};
__this.trunc = function() {
    var __data = _.parse_args(arguments, ['s'], []);
    var __output = '';
    __output += _.escape(jinja2filters.string(__data.s));
    return __output;
};
__ns['string_filter'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
