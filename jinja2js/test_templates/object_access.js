goog.provide('j2.object_access');

j2.object_access.test_obj = function(__data) {
    var obj = __data.obj;
    goog.asserts.assert(goog.isDef(obj), "Required parameter not provided: obj");
    var __output = '';
    __output += _.escape(obj['a']);
    return __output;
};