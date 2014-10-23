goog.provide('j2.object_access');

j2.object_access.test_obj = function() {
    var __data = _.parse_args(arguments, ['obj'], []);
    var __output = '';
    __output += _.escape(__data.obj['a']);
    return __output;
};
