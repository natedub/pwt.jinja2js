(function(_) {
var __this = {};

__this.concat_str = function() {
    var __data = _.parse_args(arguments, ['val'], []);
    var __output = '';
    __output += '\n';
    var myvar = '' + 'prefix' + __data.val;
    __output += '\n' + _.escape(myvar) + '\n';
    return __output;
};

__this.concat_consts = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    __output += '\n';
    var myvar = '' + 'prefix' + 'else';
    __output += '\n';
    return __output;
};
j2.string_concat = __this;
})(jinja2support);
