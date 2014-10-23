(function(_) {
var __this = {};

__this.hello = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.name) + '\n';
    return __output;
};
j2.access_var = __this;
})(jinja2support);
