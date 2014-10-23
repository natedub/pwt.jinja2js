goog.provide('j2.object_access_double_quote');

j2.object_access_double_quote.test_obj = function(__data) {
    var __output = '';
    __output += _.escape(__data.obj['a']);
    return __output;
};
