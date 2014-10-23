goog.provide('j2.import');


goog.require('j2.call_macro');


j2.import.mac = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + j2.call_macro.testcall() + '\n';
    return __output;
};
