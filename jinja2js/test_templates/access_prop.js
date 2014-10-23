(function(_) {
var __this = {};

__this.hello = function() {
    var __data = _.parse_args(arguments, ['person'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.person.name) + '\n';
    return __output;
};
j2.access_prop = __this;
})(jinja2support);
