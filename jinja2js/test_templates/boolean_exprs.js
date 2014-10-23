goog.provide('j2.boolean_exprs');

j2.boolean_exprs.test_and = function(__data) {
    var a = __data.a;
    var b = __data.b;
    var __output = '';
    if (_.truth(a) && _.truth(b)) {
        __output += 'True';
    }
    return __output;
};

j2.boolean_exprs.test_or = function(__data) {
    var a = __data.a;
    var b = __data.b;
    var __output = '';
    if (_.truth(a) || _.truth(b)) {
        __output += 'True';
    }
    return __output;
};

j2.boolean_exprs.test_xor = function(__data) {
    var a = __data.a;
    var b = __data.b;
    var __output = '';
    if ((_.truth(a) || _.truth(b)) && !(_.truth(a) && _.truth(b))) {
        __output += 'True';
    }
    return __output;
};

j2.boolean_exprs.test_alt_xor = function(__data) {
    var a = __data.a;
    var b = __data.b;
    var __output = '';
    if ((_.not(a) && _.truth(b)) || (_.truth(a) && _.not(b))) {
        __output += 'True';
    }
    return __output;
};