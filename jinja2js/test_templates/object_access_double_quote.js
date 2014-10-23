goog.provide('j2.object_access_double_quote');

j2.object_access_double_quote.test_obj = function(__data) {
    var obj = __data.obj;
    goog.asserts.assert(goog.isDef(obj), "Required parameter not provided: obj");
    var __output = '';
    __output += _.escape(obj['a']);
    return __output;
};