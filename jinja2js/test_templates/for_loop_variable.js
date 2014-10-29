goog.provide('j2.for_loop_variable');

j2.for_loop_variable.for_loop_var_index = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.escape(__iIndex + 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_index0 = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.escape(__iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.escape(__iListLength - __iIndex - 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex0 = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.escape(__iListLength - __iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_first = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.escape(!__iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_last = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.escape(__iIndex == (__iListLength - 1));
    }
    return __output;
};


j2.for_loop_variable.for_loop_var_length = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.escape(__iListLength);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_cycle = function(__data) {
    var items = __data.items;
    goog.asserts.assert(goog.isDef(items), "Required parameter not provided: items");
    var __output = '';
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.cycle(__iIndex, ['odd', 'even']);
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
    var __iList = items;
    var __iListLength = __iList.length;
    for (var __iIndex = 0; __iIndex < __iListLength; ++__iIndex) {
        var i = __iList[__iIndex];
        __output += _.cycle(__iIndex, [var1, var2]);
    }
    return __output;
};