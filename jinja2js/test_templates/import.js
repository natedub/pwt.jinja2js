(function(__ns, _) {
var __this = {};

var macs = __ns['admin/macros'];

__this.mac = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + macs.other_mac() + '\n';
    return __output;
};
__ns['import'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
