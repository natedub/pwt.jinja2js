goog.provide('j2.call_macro');

j2.call_macro.testif = function(__data) {
    var option = __data.option;
    goog.asserts.assert(goog.isDef(option), "Required parameter not provided: option");
    var __output = '';
    if (_.truth(option)) {
        __output += '\n' + _.escape(option) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.call_macro.testcall = function(__data) {
    var __output = '';
    __output += '\n' + j2.call_macro.testif() + '\n';
    return __output;
};