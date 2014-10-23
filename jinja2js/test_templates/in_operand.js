goog.provide('j2.in_operand');

j2.in_operand.test_in = function(__data) {
    var name = __data.name;
    goog.asserts.assert(goog.isDef(name), "Required parameter not provided: name");
    var __output = '';
    if (_.in_(name, ['bob', 'john'])) {
        __output += 'Yes';
    }
    return __output;
};

j2.in_operand.test_not_in = function(__data) {
    var name = __data.name;
    goog.asserts.assert(goog.isDef(name), "Required parameter not provided: name");
    var __output = '';
    if (!_.in_(name, ['bob', 'john'])) {
        __output += 'No';
    }
    return __output;
};