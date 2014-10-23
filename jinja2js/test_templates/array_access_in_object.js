goog.provide('j2.array_access_in_object');

j2.array_access_in_object.test_array_dot = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.items.large[0].name) + '\n';
    return __output;
};
