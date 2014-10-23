goog.provide('j2.access_prop');

j2.access_prop.hello = function() {
    var __data = _.parse_args(arguments, ['person'], []);
    var __output = '';
    __output += '\n' + _.escape(__data.person.name) + '\n';
    return __output;
};
