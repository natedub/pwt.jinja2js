(function(__ns, _) {
var __this = {};
__this.hello = function() {
    var __data = _.parse_args(arguments, ['person'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.person.name) + '\n';
    return __output;
};
__ns['access_prop'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
