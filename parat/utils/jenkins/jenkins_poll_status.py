import asyncio
import logging
import os
from typing import Any

from parat.constants import END, JENKINS_USER, JENKINS_TOKEN, BUILD, HOSTS, JOBS, URL
from parat.enums.jenkins import JenkinsJobStatus
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins.jenkins_utils import get_jenkins_job_dict_url_end_build_number


async def update_build_jobs_tracking_dict(build_jobs_statuses: tuple[Any], build_jobs_tracking_dict: dict):
    for build_job_status in build_jobs_statuses:
        for host in build_jobs_tracking_dict[BUILD][HOSTS]:
            for job in host[JOBS]:
                if build_job_status['host'] == host[URL] and build_job_status[END] == job[END] and build_job_status['build_number'] == job['build_index']:
                    job['status'] = build_job_status['status'].name


async def track_multiple_build_job_statuses(build_jobs_tracking_dict: dict):
    url_combos: list[dict] = []
    for host_index in range(len(build_jobs_tracking_dict[BUILD][HOSTS])):
        host = build_jobs_tracking_dict[BUILD][HOSTS][host_index]
        for job_index in range(len(build_jobs_tracking_dict[BUILD][HOSTS][host_index][JOBS])):
            job = build_jobs_tracking_dict[BUILD][HOSTS][host_index][JOBS][job_index]
            url_combos.append({'host': host, 'job': {'end': job['end'], 'build_index': job['build_index']}})
    call_list = [poll_jenkins_job_for_success_or_unstable_status(
        JenkinsRequestSettings(url_combo['host'][URL], (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)), 1),
        url_combo['job']['end'], url_combo['job']['build_index']
    ) for url_combo in url_combos]
    statuses = await asyncio.gather(*call_list)
    await update_build_jobs_tracking_dict(statuses, build_jobs_tracking_dict)


async def poll_jenkins_job_for_success_or_unstable_status(jenkins_request_settings: JenkinsRequestSettings,
                                                          url_end: str,
                                                          build_number: int) -> dict:
    jenkins_job_status: JenkinsJobStatus = JenkinsJobStatus.UNKNOWN
    none_responses_count = 0
    unknown_responses_count = 0
    should_poll = True
    while should_poll:
        response_dict = get_jenkins_job_dict_url_end_build_number(jenkins_request_settings, url_end, build_number)
        if response_dict is None:
            logging.info(f'None response for {url_end} #{build_number}')
            none_responses_count += 1
            if none_responses_count >= 5:
                logging.info(f'None response for {url_end} #{build_number} None Response #{none_responses_count}')
                jenkins_job_status = JenkinsJobStatus.UNKNOWN
                logging.error(
                    f'Result of {url_end} #{build_number} is None for the last {none_responses_count} attempts, stopping polling!')
                break
            else:
                logging.info(
                    f'Continuing to poll {url_end} #{build_number} with status None response for attempt #{none_responses_count + 1}')
                await asyncio.sleep(60)
        elif response_dict['result'] == 'SUCCESS':
            jenkins_job_status = JenkinsJobStatus.SUCCESS
            logging.info(f'Result of {url_end} #{build_number} is {jenkins_job_status}, stopping polling!')
            break
        elif response_dict['result'] == 'UNSTABLE':
            jenkins_job_status = JenkinsJobStatus.UNSTABLE
            logging.info(f'Result of {url_end} #{build_number} is {jenkins_job_status}, stopping polling!')
            break
        elif response_dict['result'] == 'UNKNOWN':
            logging.info(f'UNKNOWN for {url_end} #{build_number}')
            unknown_responses_count += 1
            if unknown_responses_count >= 5:
                logging.info(f'UNKNOWN for {url_end} #{build_number} {unknown_responses_count=}')
                jenkins_job_status = JenkinsJobStatus.UNKNOWN
                logging.error(
                    f'Result of {url_end} #{build_number} is {jenkins_job_status} for the last {unknown_responses_count} attempts, stopping polling!')
                break
            else:
                logging.info(
                    f'Continuing to poll {url_end} #{build_number} with status UNKNOWN for attempt #{unknown_responses_count + 1}')
                await asyncio.sleep(60)
        elif response_dict['result'] == 'FAILURE':
            jenkins_job_status = JenkinsJobStatus.FAILURE
            logging.error(f'Result of {url_end} #{build_number} is {jenkins_job_status}, stopping polling!')
            break
        elif response_dict['result'] == 'ABORTED':
            jenkins_job_status = JenkinsJobStatus.ABORTED
            logging.error(f'Result of {url_end} #{build_number} is {jenkins_job_status}, stopping polling!')
        else:
            logging.info(f'Continuing to poll {url_end} #{build_number} with status: {response_dict["result"]}...')
            await asyncio.sleep(60)
    logging.info(f'Polling for {url_end} #{build_number} complete with status {jenkins_job_status}!')
    return {'host': jenkins_request_settings.url, END: url_end, 'build_number': build_number,
            'status': jenkins_job_status}
