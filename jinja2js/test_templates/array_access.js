goog.provide('j2.array_access');

j2.array_access.test_array = function(__data) {
    var items = __data.items;
    var __output = '';
    __output += _.escape(items[0]);
    return __output;
};