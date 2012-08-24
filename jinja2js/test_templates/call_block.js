(function(jinja2js) {
jinja2js.render_dialog = function() {
    var __data = jinja2support.parse_args(arguments, ['type']);
    var __output = '';
    __output += '<div class="type">' + __data.__caller() + '</div>';
    return __output;
};

jinja2js.render = function() {
    var __data = jinja2support.parse_args(arguments, ['name']);
    var __output = '';
    func_caller = function() {
        var __output = '';
        __output += 'Hello ' + jinja2support.escape(__data.name) + '!';
        return __output;
    };
    __output += jinja2js.render_dialog('box', null, func_caller);
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
