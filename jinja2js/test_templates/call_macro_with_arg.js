(function(__ns, _) {
__ns.testif = function() {
    var __data = _.parse_args(arguments, ['option']);
    var __output = '';
    if (_.truth(__data.option)) {
        __output += '\n' + _.escape(__data.option) + '\n';
    }
    __output += '\n';
    return __output;
};

__ns.testcall = function() {
    var __data = _.parse_args(arguments, []);
    var __output = '';
    __output += '\n' + __ns.testif(true) + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
