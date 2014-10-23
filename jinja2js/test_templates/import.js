goog.provide('j2.import');


goog.require('j2.call_macro');


j2.import.mac = function(__data) {
    var __output = '';
    __output += '\n' + j2.call_macro.testcall() + '\n';
    return __output;
};
