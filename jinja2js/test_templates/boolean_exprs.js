(function(__ns, _) {
__ns.test_and = function() {
    var __data = _.parse_args(arguments, ['foo', 'bar']);
    var __output = '';
    if (!_.not(!_.not(__data.foo) && !_.not(__data.bar))) {
        __output += 'True';
    }
    return __output;
};

__ns.test_or = function() {
    var __data = _.parse_args(arguments, ['foo', 'bar']);
    var __output = '';
    if (!_.not(!_.not(__data.foo) || !_.not(__data.bar))) {
        __output += 'True';
    }
    return __output;
};

__ns.test_xor = function() {
    var __data = _.parse_args(arguments, ['foo', 'bar']);
    var __output = '';
    if (!_.not(!_.not(!_.not(__data.foo) || !_.not(__data.bar)) && !_.not(!(!_.not(__data.foo) && !_.not(__data.bar))))) {
        __output += 'True';
    }
    return __output;
};
})(window.jinja2js = window.jinja2js || {}, jinja2support);
