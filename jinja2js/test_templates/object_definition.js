(function(__ns, _) {
var __this = {};
__this.object_definition = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {'a': 'b', 'b': 'c'};
    return __output;
};

__this.object_definition_with_varible_value = function() {
    var __data = _.parse_args(arguments, ['val'], []);
    var __output = '';
    var a = {'a': __data.val, 'b': 'c'};
    return __output;
};

__this.object_definition_with_dot_in_key = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {'a.b': 'b', 'b': 'c'};
    return __output;
};

__this.object_definition_with_quotes_in_key = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {"'a.b'": 'b', '"b"': 'c', 'b"\'': 'b"\'', 'b\'"': 'b\'"'};
    return __output;
};

__this.object_definition_with_numbers_in_key = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {1: 'b', 3: 'c'};
    return __output;
};
__ns['object_definition'] = __this;
})(this.jinja2js = this.jinja2js || {}, jinja2support);
