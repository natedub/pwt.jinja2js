goog.provide('j2.boolean_exprs');

j2.boolean_exprs.test_and = function(__data) {
    var __output = '';
    if (_.truth(__data.a) && _.truth(__data.b)) {
        __output += 'True';
    }
    return __output;
};

j2.boolean_exprs.test_or = function(__data) {
    var __output = '';
    if (_.truth(__data.a) || _.truth(__data.b)) {
        __output += 'True';
    }
    return __output;
};

j2.boolean_exprs.test_xor = function(__data) {
    var __output = '';
    if ((_.truth(__data.a) || _.truth(__data.b)) && !(_.truth(__data.a) && _.truth(__data.b))) {
        __output += 'True';
    }
    return __output;
};

j2.boolean_exprs.test_alt_xor = function(__data) {
    var __output = '';
    if ((_.not(__data.a) && _.truth(__data.b)) || (_.truth(__data.a) && _.not(__data.b))) {
        __output += 'True';
    }
    return __output;
};
