(function(__ns, _) {
var __this = {};
__this.default_macro = function() {
    var __data = _.parse_args(arguments, [], [['foo', 'bar']]);
    var __output = '';
    __output += '\n' + _.escape(__data.foo) + '\n';
    return __output;
};

__this.mixed_macro = function() {
    var __data = _.parse_args(arguments, ['foo'], [['bar', 'baz']]);
    var __output = '';
    __output += '\n' + _.escape(__data.foo) + '\n';
    return __output;
};

__this.test_call_default_macro_with_arg = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + __this.default_macro('hello') + '\n';
    return __output;
};

__this.test_call_default_macro_with_kwarg = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + __this.default_macro({'__jinja2_kwargs__': true, 'foo': 'hello'}) + '\n';
    return __output;
};

__this.test_call_mixed_macro_with_arg = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + __this.mixed_macro('hello') + '\n';
    return __output;
};

__this.test_call_mixed_macro_with_kwarg = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + __this.mixed_macro('hello', {'__jinja2_kwargs__': true, 'bar': 'goodbye'}) + '\n';
    return __output;
};
__ns['keyword_args'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
