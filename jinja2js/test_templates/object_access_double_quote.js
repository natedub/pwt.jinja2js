(function(_) {
var __this = {};

__this.test_obj = function() {
    var __data = _.parse_args(arguments, ['obj'], []);
    var __output = '';
    __output += _.escape(__data.obj['a']);
    return __output;
};
j2.object_access_double_quote = __this;
})(jinja2support);
