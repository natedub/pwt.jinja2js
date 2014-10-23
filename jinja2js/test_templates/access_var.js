goog.provide('j2.access_var');

j2.access_var.hello = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.name) + '\n';
    return __output;
};
