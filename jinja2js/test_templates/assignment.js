goog.provide('j2.assignment');

j2.assignment.test_assignment = function(__data) {
    var __output = '';
    __output += '\n';
    var value = 1;
    __output += '\n' + _.escape(value) + '\n';
    value = 2;
    __output += '\n' + _.escape(value) + '\n';
    return __output;
};

j2.assignment.test_assignment_param = function(__data) {
    var param = __data.param;
    var __output = '';
    __output += '\n';
    param = (param + '?');
    __output += '\n' + _.escape(param) + '\n';
    return __output;
};