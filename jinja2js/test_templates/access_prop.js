(function(jinja2js) {
jinja2js.hello = function() {
    var __data = jinja2support.parse_args(arguments, ['person']);
    var __output = '';
    __output += '\n' + __data.person.name + '\n';
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
