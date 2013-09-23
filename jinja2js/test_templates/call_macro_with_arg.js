(function(__ns, _) {
var __this = {};
__this.testif = function() {
    var __data = _.parse_args(arguments, ['option'], []);
    var __output = '';
    if (_.truth(__data.option)) {
        __output += '\n' + _.escape(__data.option) + '\n';
    }
    __output += '\n';
    return __output;
};

__this.testcall = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n' + __this.testif({'__jinja2_kwargs__': true, 'option': true}) + '\n';
    return __output;
};
__ns['call_macro_with_arg'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
