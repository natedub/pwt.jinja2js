goog.provide('j2.object_access_with_named_var');

j2.object_access_with_named_var.test_named_access = function(__data) {
    var __output = '';
    __output += '\n';
    var tList = __data.allowed_types;
    var tListLen = tList.length;
    for (var tIndex = 0; tIndex < tListLen; tIndex++) {
        var tData = tList[tIndex];
        __output += '\n' + _.escape(__data.types[tData]) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.object_access_with_named_var.test_named_access_sub_value = function(__data) {
    var __output = '';
    __output += '\n';
    var tList = __data.allowed_types;
    var tListLen = tList.length;
    for (var tIndex = 0; tIndex < tListLen; tIndex++) {
        var tData = tList[tIndex];
        __output += '\n' + _.escape(__data.types[tData.name]) + '\n';
    }
    __output += '\n';
    return __output;
};

j2.object_access_with_named_var.test_named_access_assigned_value = function(__data) {
    var __output = '';
    __output += '\n';
    var types = {'h1': 'H1'};
    __output += '\n';
    var tList = __data.allowed_types;
    var tListLen = tList.length;
    for (var tIndex = 0; tIndex < tListLen; tIndex++) {
        var tData = tList[tIndex];
        __output += '\n' + _.escape(types[tData.name]) + '\n';
    }
    __output += '\n';
    return __output;
};
