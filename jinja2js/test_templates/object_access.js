(function(__ns, _) {
var __this = {};
__this.test_obj = function() {
    var __data = _.parse_args(arguments, ['obj'], []);
    var __output = '';
    __output += _.escape(__data.obj['a']);
    return __output;
};
__ns['object_access'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
