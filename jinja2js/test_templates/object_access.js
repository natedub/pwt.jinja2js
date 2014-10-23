goog.provide('j2.object_access');

j2.object_access.test_obj = function(__data) {
    var __output = '';
    __output += _.escape(__data.obj['a']);
    return __output;
};
