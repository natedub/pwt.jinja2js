goog.provide('j2.access_var');

j2.access_var.hello = function(__data) {
    var __output = '';
    __output += '\n' + _.escape(__data.name) + '\n';
    return __output;
};
