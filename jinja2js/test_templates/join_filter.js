goog.provide('j2.join_filter');

j2.join_filter.join_filter_default = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c']));
    return __output;
};

j2.join_filter.join_filter = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], ','));
    return __output;
};

j2.join_filter.join_filter_kwarg = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], {'__jinja2_kwargs__': true, 'd': ','}));
    return __output;
};

j2.join_filter.join_filter_var_arg = function() {
    var __data = _.parse_args(arguments, ['separator'], []);
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], __data.separator));
    return __output;
};

j2.join_filter.join_filter_array_arg = function() {
    var __data = _.parse_args(arguments, ['separators', 'index'], []);
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], __data.separators[__data.index]));
    return __output;
};

j2.join_filter.join_filter_complex_arg = function() {
    var __data = _.parse_args(arguments, ['config', 'type'], []);
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], __data.config.separator[__data.type].value));
    return __output;
};