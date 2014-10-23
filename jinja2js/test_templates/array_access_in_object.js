goog.provide('j2.array_access_in_object');

j2.array_access_in_object.test_array_dot = function(__data) {
    var items = __data.items;
    var __output = '';
    __output += '\n' + _.escape(items.large[0].name) + '\n';
    return __output;
};