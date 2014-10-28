goog.provide('j2.for_loop');

j2.for_loop.forinlist = function(__data) {
    var jobs = __data.jobs;
    goog.asserts.assert(goog.isDef(jobs), "Required parameter not provided: jobs");
    var __output = '';
    var __jobList = jobs;
    var __jobListLength = __jobList.length;
    for (var __jobIndex = 0; __jobIndex < __jobListLength; ++__jobIndex) {
        var job = __jobList[__jobIndex];
        __output += '\n' + _.escape(job.name) + ' does ' + _.escape(jobData.name) + '\n';
    }
    return __output;
};