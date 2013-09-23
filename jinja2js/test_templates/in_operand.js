(function(__ns, _) {
var __this = {};
__this.test_in = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    if (_.in_(__data.name, ['bob', 'john'])) {
        __output += 'Yes';
    }
    return __output;
};

__this.test_not_in = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    if (!_.in_(__data.name, ['bob', 'john'])) {
        __output += 'No';
    }
    return __output;
};
__ns['in_operand'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
