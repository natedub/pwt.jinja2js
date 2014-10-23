goog.provide('j2.round_filter');

j2.round_filter.round_num = function(__data) {
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.round(__data.num)) + '\n';
    return __output;
};

j2.round_filter.round_num_kwarg = function(__data) {
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.round(__data.num, {'__jinja2_kwargs__': true, 'precision': 2})) + '\n';
    return __output;
};

j2.round_filter.round_num_kwargs = function(__data) {
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.round(__data.num, {'__jinja2_kwargs__': true, 'precision': 2, 'method': 'floor'})) + '\n';
    return __output;
};
