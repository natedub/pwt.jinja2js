(function(__ns, _) {
__ns.test_array_dot = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.items.large[0].name) + '\n';
    return __output;
};
})(this.jinja2js = this.jinja2js || {}, jinja2support);
