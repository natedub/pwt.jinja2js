goog.provide('j2.assignment');

j2.assignment.test_assignment = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n';
    var value = 1;
    __output += '\n' + _.escape(value) + '\n';
    value = 2;
    __output += '\n' + _.escape(value) + '\n';
    return __output;
};