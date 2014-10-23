goog.provide('j2.for_loop');

j2.for_loop.forinlist = function(__data) {
    var jobs = __data.jobs;
    goog.asserts.assert(goog.isDef(jobs), "Required parameter not provided: jobs");
    var __output = '';
    var jobList = jobs;
    var jobListLen = jobList.length;
    for (var jobIndex = 0; jobIndex < jobListLen; jobIndex++) {
        var jobData = jobList[jobIndex];
        __output += '\n' + _.escape(jobData.name) + ' does ' + _.escape(jobData.name) + '\n';
    }
    return __output;
};