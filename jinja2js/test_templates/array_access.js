(function(_) {
var __this = {};

__this.test_array = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    __output += _.escape(__data.items[0]);
    return __output;
};
j2.array_access = __this;
})(jinja2support);
