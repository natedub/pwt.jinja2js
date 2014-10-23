goog.provide('j2.array_access');

j2.array_access.test_array = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    __output += _.escape(__data.items[0]);
    return __output;
};
