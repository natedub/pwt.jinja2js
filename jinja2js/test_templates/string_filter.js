goog.provide('j2.string_filter');

j2.string_filter.trunc = function(__data) {
    var __output = '';
    __output += _.escape(jinja2filters.string(__data.s));
    return __output;
};
