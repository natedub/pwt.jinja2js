goog.provide('j2.in_operand');

j2.in_operand.test_in = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    if (_.in_(__data.name, ['bob', 'john'])) {
        __output += 'Yes';
    }
    return __output;
};

j2.in_operand.test_not_in = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    if (!_.in_(__data.name, ['bob', 'john'])) {
        __output += 'No';
    }
    return __output;
};
