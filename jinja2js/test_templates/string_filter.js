goog.provide('j2.string_filter');

j2.string_filter.trunc = function(__data) {
    var s = __data.s;
    var __output = '';
    __output += _.escape(jinja2filters.string(s));
    return __output;
};