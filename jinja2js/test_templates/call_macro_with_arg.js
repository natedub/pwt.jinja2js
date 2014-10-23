goog.provide('j2.call_macro_with_arg');

j2.call_macro_with_arg.testif = function(__data) {
    var __output = '';
    if (_.truth(__data.option)) {
        __output += '\n' + _.escape(__data.option) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.call_macro_with_arg.testcall = function(__data) {
    var __output = '';
    __output += '\n' + j2.call_macro_with_arg.testif({'__jinja2_kwargs__': true, 'option': true}) + '\n';
    return __output;
};
