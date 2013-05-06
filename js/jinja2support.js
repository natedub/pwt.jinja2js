(function(jinja2support) {
    var toString = Object.prototype.toString;
    var has = Object.prototype.hasOwnProperty;
    var indexOf = Array.prototype.indexOf;

    function object_matches_kwargspec(obj, kwargspec) {
        var keys = [];
        for (var i = 0, l = kwargspec.length; i < l; i++) {
            keys.push(kwargspec[i][0]);
        }
        for (key in obj) {
            if (has.call(obj, key) && !jinja2support.in_(key, obj)) {
                return false;
            }
        }
        return true;
    }

    jinja2support.parse_args = function(args, argspec, kwargspec) {
        var data = {};
        var args_len = args.length;

        if (typeof(args[args_len - 1]) === 'function') {
            data.__caller = args[args.length - 1];
            args_len--;
        }

        var last_arg = args[args_len - 1];
        if (toString.call(last_arg) === '[object Object]' &&
            (has.call(last_arg, '__jinja2_kwargs__') ||
             object_matches_kwargspec(last_arg, kwargspec))) {

            args_len--;
            for (var i = 0, l = kwargspec.length; i < l; i++) {
                var key = kwargspec[i][0];
                var value = kwargspec[i][1];

                data[key] = has.call(last_arg, key) ? last_arg[key] : value;
            }
        } else {
            for (var i = 0, l = kwargspec.length; i < l; i++) {
                var key = kwargspec[i][0];
                var value = kwargspec[i][1];

                data[key] = value;
            }
        }

        if (args_len < argspec.length) {
            throw 'Not enough arguments supplied, expecting ' +
                argspec.length + ': [' + argspec.join(', ') + ']';
        }

        for (var i = 0, l = argspec.length; i < l; i++) {
            data[argspec[i]] = args[i];
        }

        if (args_len > argspec.length) {
            for (var i = 0, l = args_len - argspec.length; i < l; i++) {
                var key = kwargspec[i][0];

                data[key] = args[argspec.length + i];
            }
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

    jinja2support.in_ = function(value, collection) {
        if (toString.call(collection) === '[object Array]') {
            if (indexOf) {
                return indexOf.call(collection, value) > -1;
            }
            for (var i = 0, l = collection.length; i < l; i++) {
                if (collection[i] === value) {
                    return true;
                }
            }
        }
        return has.call(collection, value);
    };

    jinja2support.not = function(value) {
        var type = toString.call(value);
        if (type === '[object Array]') return !value.length;
        if (type === '[object Object]') {
            for (var prop in value) if (has.call(value, prop)) return false;
            return true;
        }
        return !value;
    };

    jinja2support.truth = function(value) {
        return !jinja2support.not(value);
    };

    jinja2support.arg_getter = function(index) {
        return function() {
            return arguments[index % arguments.length];
        };
    };

})(this.jinja2support = this.jinja2support || {});


(function(jinja2filters, _, undefined) {

jinja2filters.string = function(str) {
    return '' + str;
};

jinja2filters['default'] = function() {
    var kwargspec = [['default_value', ''], ['boolean', true]];
    var args = _.parse_args(arguments, ['value'], kwargspec);

    if (args.value === undefined || (_.not(args.value) &&
            args['boolean'])) {
        return args.default_value;
    } else {
        return args.value;
    }
};

jinja2filters.capitalize = function(str) {
    return str.substring(0, 1).toUpperCase() + str.substring(1);
};

jinja2filters.last = function(seq) {
    return seq[seq.length - 1];
};

jinja2filters.length = function(seq) {
    return seq.length;
};

jinja2filters.replace = function() {
    var kwargspec = [['count', null]];
    var args = _.parse_args(arguments, ['str', 'old', 'new'],
            kwargspec);
    var replaced = args.str;

    if (args.count === null) {
        while (replaced.indexOf(args.old) !== -1) {
            replaced = replaced.replace(args.old, args['new']);
        }
    } else {
        for (var i = 0; i < args.count; i++) {
            replaced = replaced.replace(args.old, args['new']);
        }
    }
    return replaced;
};

jinja2filters.round = function() {
    var kwargspec = [['precision', 0], ['method', 'common']];
    var args = _.parse_args(arguments, ['value'], kwargspec);

    var precision = Math.pow(10, args.precision);
    var val = args.value * precision;
    var method = Math.round;

    if (args.method === 'ceil') {
        method = Math.ceil;
    } else if (args.method === 'floor') {
        method = Math.floor;
    }

    return method(val) / precision;
};

jinja2filters.join = function() {
    var kwargspec = [['d', ''], ['attribute', null]];
    var args = _.parse_args(arguments, ['value'], kwargspec);

    var list = args.value;
    if (args.attribute != null) {
        list = [];
        for (var i = 0, l = args.value.length; i < l; i++) {
            list.push(args.value[i][args.attribute]);
        }
    }

    return list.join(args.d);
};

jinja2filters.truncate = function() {
    var kwargspec = [['length', 255], ['killwords', false], ['end', '...']];
    var args = _.parse_args(arguments, ['s'], kwargspec);
    var len = args['length'];

    if (args.s.length < len) {
        return args.s;
    }

    if (!args.killwords) {
        var index = args.s.substring(len).indexOf(' ');
        len = index > -1 ? len + index : len;
    }

    return args.s.substring(0, len) + args.end;
};

})(this.jinja2filters = this.jinja2filters || {}, jinja2support);
