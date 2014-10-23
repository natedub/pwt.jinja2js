goog.provide('j2.call_macro');

j2.call_macro.testif = function() {
    var __data = _.parse_args(arguments, ['option'], []);
    var __output = '';
    if (_.truth(__data.option)) {
        __output += '\n' + _.escape(__data.option) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.call_macro.testcall = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + j2.call_macro.testif() + '\n';
    return __output;
};
