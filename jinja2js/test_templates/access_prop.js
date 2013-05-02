(function(__ns, _) {
__ns.hello = function() {
    var __data = _.parse_args(arguments, ['person'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.person.name) + '\n';
    return __output;
};
})(this.jinja2js = this.jinja2js || {}, jinja2support);
