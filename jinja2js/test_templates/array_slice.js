(function(__ns, _) {
var __this = {};
__this.array_slice = function() {
    var __data = _.parse_args(arguments, ['arr'], []);
    var __output = '';
    __output += _.escape(__data.arr.slice(0, 4));
    return __output;
};

__this.array_slice_no_start = function() {
    var __data = _.parse_args(arguments, ['arr'], []);
    var __output = '';
    __output += _.escape(__data.arr.slice(0, 4));
    return __output;
};

__this.array_slice_no_end = function() {
    var __data = _.parse_args(arguments, ['arr'], []);
    var __output = '';
    __output += _.escape(__data.arr.slice(1));
    return __output;
};
__ns['array_slice'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
