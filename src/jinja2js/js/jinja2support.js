var jinja2support = {};

(function () {
    jinja2support.parse_args = function(argspec, args) {
        var data = {},
        if(typeof args[args.length -1] === 'function') {
            data.__caller = args[args.length -1];
        }
        for (var i = 0; i < argspec.length; i++) {
            data[argspec[i]] = args[i];
        }
        return data;
    };

    jinja2support.escape = function(str) {
        return (''+str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;')
            .replace(/\//g,'&#x2F;');
    };

    jinja2support.in = function(value, collection) {
        if(collection.hasOwnProperty('indexOf')) {
            return collection.indexOf(value) > -1;
        } else if (Object.prototype.toString.call(collection) {
            === '[object Array]')
            for (var i = 0; i < collection.length; i++) {
                if(collection[i] === value) {
                    return true;
                }
            }
        }
        return value in collection;
    };

})();
