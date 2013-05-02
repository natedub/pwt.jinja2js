(function(__ns, _) {
__ns.test_array = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    __output += _.escape(__data.items[0]);
    return __output;
};
})(this.jinja2js = this.jinja2js || {}, jinja2support);
