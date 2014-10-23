goog.provide('j2.call_macro_with_arg');

j2.call_macro_with_arg.testif = function(__data) {
    var option = __data.option;
    goog.asserts.assert(goog.isDef(option), "Required parameter not provided: option");
    var __output = '';
    if (_.truth(option)) {
        __output += '\n' + _.escape(option) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.call_macro_with_arg.testcall = function(__data) {
    var __output = '';
    __output += '\n' + j2.call_macro_with_arg.testif({'__jinja2_kwargs__': true, 'option': true}) + '\n';
    return __output;
};