(function(__ns, _) {
__ns.test_in = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    if (_.in_(__data.name, ['bob', 'john'])) {
        __output += 'Yes';
    }
    return __output;
};

__ns.test_not_in = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    if (!_.in_(__data.name, ['bob', 'john'])) {
        __output += 'No';
    }
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
