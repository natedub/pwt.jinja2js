(function(_) {
var __this = {};

__this.trunc = function() {
    var __data = _.parse_args(arguments, ['s'], []);
    var __output = '';
    __output += _.escape(jinja2filters.string(__data.s));
    return __output;
};
j2.string_filter = __this;
})(jinja2support);
