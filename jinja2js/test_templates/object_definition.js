goog.provide('j2.object_definition');

j2.object_definition.object_definition = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {'a': 'b', 'b': 'c'};
    return __output;
};

j2.object_definition.object_definition_with_varible_value = function() {
    var __data = _.parse_args(arguments, ['val'], []);
    var __output = '';
    var a = {'a': __data.val, 'b': 'c'};
    return __output;
};

j2.object_definition.object_definition_with_dot_in_key = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {'a.b': 'b', 'b': 'c'};
    return __output;
};

j2.object_definition.object_definition_with_quotes_in_key = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {"'a.b'": 'b', '"b"': 'c', 'b"\'': 'b"\'', 'b\'"': 'b\'"'};
    return __output;
};

j2.object_definition.object_definition_with_numbers_in_key = function() {
    var __data = _.parse_args(arguments, [], []);
    var __output = '';
    var a = {1: 'b', 3: 'c'};
    return __output;
};
