goog.provide('j2.call_block');

j2.call_block.render_dialog = function(__data) {
    var type = __data.type;
    goog.asserts.assert(goog.isDef(type), "Required parameter not provided: type");
    var __output = '';
    __output += '<div class="type">' + __data.__caller() + '</div>';
    return __output;
};

j2.call_block.render = function(__data) {
    var name = __data.name;
    goog.asserts.assert(goog.isDef(name), "Required parameter not provided: name");
    var __output = '';
    func_caller = function() {
        var __output = '';
        __output += 'Hello ' + _.escape(name) + '!';
        return __output;
    };
    __output += j2.call_block.render_dialog({'__jinja2_kwargs__': true, 'type': 'box'}, func_caller);
    return __output;
};