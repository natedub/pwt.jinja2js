goog.provide('j2.import');


goog.require('j2.keyword_args');


j2.import.test_pos_arg = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.mixed_macro({foo: 'foo_pos'}) + '\n';
    return __output;
};

j2.import.test_pos_args = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.mixed_macro({foo: 'foo_pos', bar: 'bar_pos'}) + '\n';
    return __output;
};

j2.import.test_mixed_args = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.mixed_macro({foo: 'foo_arg', bar: 'bar_kw'}) + '\n';
    return __output;
};

j2.import.test_all_kwargs = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.mixed_macro({foo: 'foo_arg', bar: 'bar_kw'}) + '\n';
    return __output;
};