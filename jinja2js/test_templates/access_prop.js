goog.provide('j2.access_prop');

j2.access_prop.hello = function(__data) {
    var person = __data.person;
    var __output = '';
    __output += '\n' + _.escape(person.name) + '\n';
    return __output;
};