(function(_) {
var __this = {};

__this.render_dialog = function() {
    var __data = _.parse_args(arguments, ['type'], []);
    var __output = '';
    __output += '<div class="type">' + __data.__caller() + '</div>';
    return __output;
};

__this.render = function() {
    var __data = _.parse_args(arguments, ['name'], []);
    var __output = '';
    func_caller = function() {
        var __output = '';
        __output += 'Hello ' + _.escape(__data.name) + '!';
        return __output;
    };
    __output += __this.render_dialog({'__jinja2_kwargs__': true, 'type': 'box'}, func_caller);
    return __output;
};
j2.call_block = __this;
})(jinja2support);
