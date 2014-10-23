goog.provide('j2.for_loop_variable');

j2.for_loop_variable.for_loop_var_index = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex + 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_index0 = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen - iIndex - 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex0 = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen - iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_first = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex == 0);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_last = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex == (iListLen - 1));
    }
    return __output;
};


j2.for_loop_variable.for_loop_var_length = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_cycle = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.arg_getter(iIndex)('odd', 'even');
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_cycle_vars = function(__data) {
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.arg_getter(iIndex)(__data.var1, __data.var2);
    }
    return __output;
};
