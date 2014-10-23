goog.provide('j2.string_concat');

j2.string_concat.concat_str = function(__data) {
    var val = __data.val;
    goog.asserts.assert(goog.isDef(val), "Required parameter not provided: val");
    var __output = '';
    __output += '\n';
    var myvar = '' + 'prefix' + val;
    __output += '\n' + _.escape(myvar) + '\n';
    return __output;
};

j2.string_concat.concat_consts = function(__data) {
    var __output = '';
    __output += '\n';
    var myvar = '' + 'prefix' + 'else';
    __output += '\n';
    return __output;
};