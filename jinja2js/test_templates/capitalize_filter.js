goog.provide('j2.capitalize_filter');

j2.capitalize_filter.trunc = function() {
    var __data = _.parse_args(arguments, ['s'], []);
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.capitalize(__data.s)) + '\n';
    return __output;
};
