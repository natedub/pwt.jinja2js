(function(jinja2js) {
jinja2js.forinlist = function() {
    var __data = jinja2support.parse_args(arguments, ['jobs']);
    var __output = '';
    var jobList = __data.jobs;
    var jobListLen = jobList.length;
    for (var jobIndex = 0; jobIndex < jobListLen; jobIndex++) {
        var jobData = jobList[jobIndex];
        __output += '\n' + jinja2support.escape(jobData.name) + ' does ' + jinja2support.escape(jobData.name) + '\n';
    }
    return __output;
};
})(window.jinja2js = window.jinja2js || {});
