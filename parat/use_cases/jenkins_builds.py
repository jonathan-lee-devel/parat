import logging
import os

from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins.jenkins_utils import get_jenkins_job_dict_url_end, start_jenkins_build_url_end


def process_build_host(build_host: dict) -> dict:
    successful_jobs = []
    failed_jobs = []
    for build_job_index in range(len(build_host['jobs'])):
        build_job_url_end = build_host['jobs'][build_job_index]['end']
        jenkins_job_pre_run_dict = get_jenkins_job_dict_url_end(
            JenkinsRequestSettings(build_host['url'], (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1),
            build_job_url_end)
        build_number_to_track = None
        if jenkins_job_pre_run_dict is not None:
            build_number_to_track = len(jenkins_job_pre_run_dict['builds']) + 1
        response_status_code = start_jenkins_build_url_end(
            JenkinsRequestSettings(build_host['url'], (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')),
                                   1), build_job_url_end)
        if response_status_code == 201:
            logging.info(f'Successfully kicked off build [{build_host["url"]}] ({build_job_url_end})!')
            successful_jobs.append({'url': build_host['url'], 'end': build_job_url_end, 'index': build_job_index,
                                    'build_number': build_number_to_track})
            build_host['jobs'][build_job_index]['build_index'] = build_number_to_track
        else:
            logging.error(f'Failed to kick off build [{build_host["url"]}] ({build_job_url_end}!')
            failed_jobs.append({'url': build_host['url'], 'end': build_job_url_end, 'index': build_job_index})

    return {'successful_jobs': successful_jobs, 'failed_jobs': failed_jobs}
