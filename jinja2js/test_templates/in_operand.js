(function(__ns, _) {
__ns.test_in = function() {
    var __data = _.parse_args(arguments, ['name']);
    var __output = '';
    __output += '\n';
    if (!_.not(_.in(__data.name, ['bob', 'john']))) {
        __output += 'Yes';
    }
    __output += '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
