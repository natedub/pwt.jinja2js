goog.provide('j2.array_slice');


j2.array_slice.array_slice = function(__data) {
    var __output = '';
    __output += _.escape(__data.arr.slice(0, 4));
    return __output;
};

j2.array_slice.array_slice_no_start = function(__data) {
    var __output = '';
    __output += _.escape(__data.arr.slice(0, 4));
    return __output;
};

j2.array_slice.array_slice_no_end = function(__data) {
    var __output = '';
    __output += _.escape(__data.arr.slice(1));
    return __output;
};
