(function(__ns, _) {
__ns.testif = function() {
    var __data = _.parse_args(arguments, ['option'], []);
    var __output = '';
    if (_.truth(__data.option)) {
        __output += '\n' + _.escape(__data.option) + '\n';
    }
    __output += '\n';
    return __output;
};

__ns.testcall = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + __ns.testif() + '\n';
    return __output;
};
})(this.jinja2js = this.jinja2js || {}, jinja2support);
