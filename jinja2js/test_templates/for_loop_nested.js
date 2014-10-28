goog.provide('j2.for_loop_nested');

j2.for_loop_nested.nested_extended_loops_and_else = function(__data) {
    var json = __data.json;
    goog.asserts.assert(goog.isDef(json), "Required parameter not provided: json");
    var __output = '';
    var __rowList = json['rows'];
    var __rowListLength = __rowList.length;
    for (var __rowIndex = 0; __rowIndex < __rowListLength; ++__rowIndex) {
        var row = __rowList[__rowIndex];
        __output += _.escape(__rowIndex + 1) + ':';
        var __colList = row;
        var __colListLength = __colList.length;
        for (var __colIndex = 0; __colIndex < __colListLength; ++__colIndex) {
            var col = __colList[__colIndex];
            __output += _.escape(__rowIndex + 1) + ' x ' + _.escape(__colIndex + 1) + ' = ' + _.escape(col);
        }
        if (!__colListLength) {
            __output += 'No data';
        }
        __output += '<br>';
    }
    return __output;
};