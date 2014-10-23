goog.provide('j2.call_macro');

j2.call_macro.testif = function(__data) {
    var __output = '';
    if (_.truth(__data.option)) {
        __output += '\n' + _.escape(__data.option) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.call_macro.testcall = function(__data) {
    var __output = '';
    __output += '\n' + j2.call_macro.testif() + '\n';
    return __output;
};
