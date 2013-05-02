(function(__ns, _) {
__ns.forinlist = function() {
    var __data = _.parse_args(arguments, ['jobs'], []);
    var __output = '';
    var jobList = __data.jobs;
    var jobListLen = jobList.length;
    for (var jobIndex = 0; jobIndex < jobListLen; jobIndex++) {
        var jobData = jobList[jobIndex];
        __output += '\n' + _.escape(jobData.name) + ' does ' + _.escape(jobData.name) + '\n';
    }
    return __output;
};
})(this.jinja2js = this.jinja2js || {}, jinja2support);
