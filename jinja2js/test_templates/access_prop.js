goog.provide('j2.access_prop');

j2.access_prop.hello = function(__data) {
    var __output = '';
    __output += '\n' + _.escape(__data.person.name) + '\n';
    return __output;
};
