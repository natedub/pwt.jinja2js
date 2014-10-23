(function(_) {
var __this = {};

__this.round_num = function() {
    var __data = _.parse_args(arguments, ['num'], []);
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.round(__data.num)) + '\n';
    return __output;
};

__this.round_num_kwarg = function() {
    var __data = _.parse_args(arguments, ['num'], []);
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.round(__data.num, {'__jinja2_kwargs__': true, 'precision': 2})) + '\n';
    return __output;
};

__this.round_num_kwargs = function() {
    var __data = _.parse_args(arguments, ['num'], []);
    var __output = '';
    __output += '\n' + _.escape(jinja2filters.round(__data.num, {'__jinja2_kwargs__': true, 'precision': 2, 'method': 'floor'})) + '\n';
    return __output;
};
j2.round_filter = __this;
})(jinja2support);

