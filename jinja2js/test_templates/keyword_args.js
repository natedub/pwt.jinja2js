goog.provide('j2.keyword_args');

j2.keyword_args.default_macro = function(__data) {
    var foo = goog.isDef(__data.foo) ? __data.foo : 'bar';
    var __output = '';
    __output += '\n' + _.escape(foo) + '\n';
    return __output;
};

j2.keyword_args.mixed_macro = function(__data) {
    var foo = __data.foo;
    goog.asserts.assert(goog.isDef(foo), "Required parameter not provided: foo");
    var bar = goog.isDef(__data.bar) ? __data.bar : 'baz';
    var __output = '';
    __output += '\n' + _.escape(foo) + '\n';
    return __output;
};

j2.keyword_args.test_call_default_macro_with_arg = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.default_macro('hello') + '\n';
    return __output;
};

j2.keyword_args.test_call_default_macro_with_kwarg = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.default_macro({'__jinja2_kwargs__': true, 'foo': 'hello'}) + '\n';
    return __output;
};

j2.keyword_args.test_call_mixed_macro_with_arg = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.mixed_macro('hello') + '\n';
    return __output;
};

j2.keyword_args.test_call_mixed_macro_with_kwarg = function(__data) {
    var __output = '';
    __output += '\n' + j2.keyword_args.mixed_macro('hello', {'__jinja2_kwargs__': true, 'bar': 'goodbye'}) + '\n';
    return __output;
};