goog.provide('j2.access_var');

j2.access_var.hello = function(__data) {
    var name = __data.name;
    var __output = '';
    __output += '\n' + _.escape(name) + '\n';
    return __output;
};