goog.provide('j2.object_access_with_named_var');

j2.object_access_with_named_var.test_named_access = function(__data) {
    var types = __data.types;
    goog.asserts.assert(goog.isDef(types), "Required parameter not provided: types");
    var allowed_types = __data.allowed_types;
    goog.asserts.assert(goog.isDef(allowed_types), "Required parameter not provided: allowed_types");
    var __output = '';
    __output += '\n';
    var __tList = allowed_types;
    var __tListLength = __tList.length;
    for (var __tIndex = 0; __tIndex < __tListLength; ++__tIndex) {
        var t = __tList[__tIndex];
        __output += '\n' + _.escape(types[t]) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.object_access_with_named_var.test_named_access_sub_value = function(__data) {
    var types = __data.types;
    goog.asserts.assert(goog.isDef(types), "Required parameter not provided: types");
    var allowed_types = __data.allowed_types;
    goog.asserts.assert(goog.isDef(allowed_types), "Required parameter not provided: allowed_types");
    var __output = '';
    __output += '\n';
    var __tList = allowed_types;
    var __tListLength = __tList.length;
    for (var __tIndex = 0; __tIndex < __tListLength; ++__tIndex) {
        var t = __tList[__tIndex];
        __output += '\n' + _.escape(types[t.name]) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.object_access_with_named_var.test_named_access_assigned_value = function(__data) {
    var allowed_types = __data.allowed_types;
    goog.asserts.assert(goog.isDef(allowed_types), "Required parameter not provided: allowed_types");
    var __output = '';
    __output += '\n';
    var types = {'h1': 'H1'};
    __output += '\n';
    var __tList = allowed_types;
    var __tListLength = __tList.length;
    for (var __tIndex = 0; __tIndex < __tListLength; ++__tIndex) {
        var t = __tList[__tIndex];
        __output += '\n' + _.escape(types[t.name]) + '\n';
    }
    __output += '\n';
    return __output;
};