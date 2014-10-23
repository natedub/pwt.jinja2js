goog.provide('j2.access_prop');

j2.access_prop.hello = function(__data) {
    var person = __data.person;
    goog.asserts.assert(goog.isDef(person), "Required parameter not provided: person");
    var __output = '';
    __output += '\n' + _.escape(person.name) + '\n';
    return __output;
};