goog.provide('j2.for_loop_variable');

j2.for_loop_variable.for_loop_var_index = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex + 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_index0 = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen - iIndex - 1);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_revindex0 = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen - iIndex);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_first = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex == 0);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_last = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iIndex == (iListLen - 1));
    }
    return __output;
};


j2.for_loop_variable.for_loop_var_length = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.escape(iListLen);
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_cycle = function() {
    var __data = _.parse_args(arguments, ['items'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.arg_getter(iIndex)('odd', 'even');
    }
    return __output;
};

j2.for_loop_variable.for_loop_var_cycle_vars = function() {
    var __data = _.parse_args(arguments, ['items', 'var1', 'var2'], []);
    var __output = '';
    var iList = __data.items;
    var iListLen = iList.length;
    for (var iIndex = 0; iIndex < iListLen; iIndex++) {
        var iData = iList[iIndex];
        __output += _.arg_getter(iIndex)(__data.var1, __data.var2);
    }
    return __output;
};
