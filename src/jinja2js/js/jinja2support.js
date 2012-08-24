(function(jinja2support) {

    jinja2support.parse_args = function(args, argspec) {
        var data = {};
        if (typeof(args[args.length - 1]) === 'function') {
            data.__caller = args[args.length - 1];
        }
        for (var i = 0; i < argspec.length; i++) {
            data[argspec[i]] = args[i];
        }
        return data;
    };

    jinja2support.escape = function(str) {
        return ('' + str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;')
            .replace(/\//g, '&#x2F;');
    };

    jinja2support.in = function(value, collection) {
        if (Object.prototype.toString.call(collection) === '[object Array]') {
            if (Array.prototype.indexOf) {
                return Array.prototype.indexOf.call(collection, value) > -1;
            }
            for (var i = 0; i < collection.length; i++) {
                if (collection[i] === value) {
                    return true;
                }
            }
        }
        return value in collection;
    };

})(window.jinja2support = window.jinja2support || {});
