(function(_) {
var __this = {};


var macs = __ns['admin/macros'];

__this.mac = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + macs.other_mac() + '\n';
    return __output;
};
j2.import = __this;
})(jinja2support);
