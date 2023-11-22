"""Jenkins builds module"""
import logging
import os
from http import HTTPStatus

from parat.constants import (
    JENKINS_USER,
    JENKINS_TOKEN,
    SUCCESSFUL_JOBS,
    FAILED_JOBS,
    BUILDS,
    URL,
    JOBS,
    END
)
from parat.utils.jenkins_rest_api.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins_rest_api.jenkins_utils import (
    get_jenkins_job_dict_url_end, start_jenkins_build_url_end
)


def process_build_host(build_host: dict) -> dict:
    """Function which parses/processes build host from dict"""
    successful_jobs = []
    failed_jobs = []
    for build_job_index in range(len(build_host[JOBS])):
        build_job_url_end = build_host[JOBS][build_job_index][END]
        jenkins_job_pre_run_dict = get_jenkins_job_dict_url_end(
            JenkinsRequestSettings(
                build_host[URL],
                (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)),
                1
            ),
            build_job_url_end)
        build_number_to_track = 0
        if jenkins_job_pre_run_dict is not None:
            builds_sorted_by_build_number = sorted(jenkins_job_pre_run_dict[BUILDS],
                                                   key=lambda x: x['number'], reverse=True)
            if jenkins_job_pre_run_dict is not None and len(builds_sorted_by_build_number) > 0:
                build_number_to_track = builds_sorted_by_build_number[0]['number'] + 1
            response_status_code = start_jenkins_build_url_end(
                JenkinsRequestSettings(
                    build_host[URL],
                    (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)),
                    1
                ), build_job_url_end)
            if response_status_code == HTTPStatus.CREATED:
                logging.info(
                    'Successfully kicked off build [%s] (%s)!',
                    build_host[URL],
                    build_job_url_end
                )
                successful_jobs.append(
                    {URL: build_host[URL],
                     END: build_job_url_end,
                     'index': build_job_index,
                     'build_number': build_number_to_track}
                )
                build_host[JOBS][build_job_index]['build_index'] = build_number_to_track
            else:
                logging.error(
                    'Failed to kick off build [%s] (%s)!',
                    build_host[URL],
                    build_job_url_end
                )
                failed_jobs.append(
                    {URL: build_host[URL],
                     END: build_job_url_end,
                     'index': build_job_index}
                )
        else:
            logging.error('Failed to kick off build [%s] (%s)!',
                          build_host[URL],
                          build_job_url_end)
            failed_jobs.append(
                {URL: build_host[URL],
                 END: build_job_url_end,
                 'index': build_job_index}
            )

    return {SUCCESSFUL_JOBS: successful_jobs, FAILED_JOBS: failed_jobs}
