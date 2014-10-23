goog.provide('j2.join_filter');

j2.join_filter.join_filter_default = function(__data) {
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c']));
    return __output;
};

j2.join_filter.join_filter = function(__data) {
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], ','));
    return __output;
};

j2.join_filter.join_filter_kwarg = function(__data) {
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], {'__jinja2_kwargs__': true, 'd': ','}));
    return __output;
};

j2.join_filter.join_filter_var_arg = function(__data) {
    var separator = __data.separator;
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], separator));
    return __output;
};

j2.join_filter.join_filter_array_arg = function(__data) {
    var separators = __data.separators;
    var index = __data.index;
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], separators[index]));
    return __output;
};

j2.join_filter.join_filter_complex_arg = function(__data) {
    var config = __data.config;
    var type = __data.type;
    var __output = '';
    __output += _.escape(jinja2filters.join(['a', 'b', 'c'], config.separator[type].value));
    return __output;
};