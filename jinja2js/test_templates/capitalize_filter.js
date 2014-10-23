goog.provide('j2.capitalize_filter');

j2.capitalize_filter.trunc = function(__data) {
    var s = __data.s;
    goog.asserts.assert(goog.isDef(s), "Required parameter not provided: s");
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.capitalize(s)) + '\n';
    return __output;
};