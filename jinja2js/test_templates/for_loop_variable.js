goog.provide('j2.for_loop_variable');

j2.for_loop_variable.for_loop_var_index = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex + 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_index0 = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen - iIndex - 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex0 = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen - iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_first = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex == 0);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_last = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex == (iListLen - 1));
    }
    return __output;
};


j2.for_loop_variable.for_loop_var_length = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_cycle = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.arg_getter(iIndex)('odd', 'even');
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_cycle_vars = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var var1 = __data.var1;
    goog.asserts.assert(goog.isDef(var1), "Required parameter not provided: var1");
    var var2 = __data.var2;
    goog.asserts.assert(goog.isDef(var2), "Required parameter not provided: var2");
    var __output = '';
    var iList = items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.arg_getter(iIndex)(var1, var2);
    }
    return __output;
};