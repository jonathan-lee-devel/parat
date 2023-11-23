"""Jenkins REST API CLI commands module"""
import asyncio
import logging
import os
import sys
from http import HTTPStatus

import click
import yaml
from dotenv import load_dotenv

from parat.cli.options import (
    verbose_option, job_name_option, build_number_option, url_end_option,
    build_jobs_yaml_file_option, trim_url_end_option_util,
    build_jobs_tracking_yaml_file_option
)
from parat.constants import (
    BUILD, HOSTS, JENKINS_URL, JENKINS_USER,
    JENKINS_TOKEN, SUCCESSFUL_JOBS, FAILED_JOBS
)
from parat.use_cases.jenkins_build_job_tracking import validate_jenkins_job_build_tracking_yaml
from parat.use_cases.jenkins_builds import process_build_host
from parat.use_cases.jenkins_job_info import get_jenkins_job_result_status
from parat.utils.jenkins_rest_api.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins_rest_api.jenkins_poll_status import track_multiple_build_job_statuses
from parat.utils.jenkins_rest_api.jenkins_utils import (
    get_jenkins_console_output, get_jenkins_job_dict,
    start_jenkins_build,
    start_jenkins_build_url_end
)
from parat.utils.logging_utils import initialize_logging, logging_line_break


@click.group(name='jenkins_rest_api')
def jenkins_commands() -> None:
    """Entry point"""


@jenkins_commands.command()
@verbose_option
@job_name_option
def start_build(verbose: bool, job_name: str) -> None:
    """Kicks off a Jenkins job build based on job name"""
    load_dotenv()
    initialize_logging(verbose)
    logging.info('Kicking off build (%s)...', job_name)
    response_status_code = start_jenkins_build(
        JenkinsRequestSettings(
            os.getenv(JENKINS_URL),
            (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)),
            1),
        job_name).status_code
    if response_status_code == HTTPStatus.CREATED:
        logging.info('Successfully kicked off build (%s)!', job_name)
    else:
        logging.error('Failed to kick off build (%s)!', job_name)


@jenkins_commands.command()
@verbose_option
@url_end_option
def start_build_url(verbose: bool, url_end: str) -> None:
    """Starts Jenkins job based on URL ending"""
    load_dotenv()
    initialize_logging(verbose)
    url_end = trim_url_end_option_util(url_end)
    logging.info('Kicking off build (%s)...', url_end)
    response_status_code = start_jenkins_build_url_end(
        JenkinsRequestSettings(
            os.getenv(JENKINS_URL),
            (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)),
            1),
        url_end)
    if response_status_code == HTTPStatus.CREATED:
        logging.info('Successfully kicked off build (%s)!', url_end)
    else:
        logging.error('Failed to kick off build (%s)!', url_end)


@jenkins_commands.command()
@verbose_option
@build_jobs_yaml_file_option
def start_build_jobs_yaml(verbose: bool, build_jobs_yaml: str) -> None:
    """Kicks off Jenkins jobs based on YAML input"""
    load_dotenv()
    initialize_logging(verbose)
    logging.info('Parsing YAML: %s...', build_jobs_yaml)
    successful_jobs = []
    failed_jobs = []
    with open(build_jobs_yaml, 'r', encoding='utf-8') as yaml_file_contents:
        build_jobs_dict = yaml.safe_load(yaml_file_contents)
        remaining_builds_dict = build_jobs_dict
        for build_host_index in range(len(build_jobs_dict[BUILD][HOSTS])):
            build_host = build_jobs_dict[BUILD][HOSTS][build_host_index]
            jobs_info_dict = process_build_host(build_host)
            successful_jobs.append(jobs_info_dict[SUCCESSFUL_JOBS])
            failed_jobs.append(jobs_info_dict[FAILED_JOBS])
    logging_line_break()
    logging.info('Run of %s completed:', build_jobs_yaml)
    logging.debug('Successful builds: %s', jobs_info_dict[SUCCESSFUL_JOBS])
    tracking_output_filename = build_jobs_yaml.replace('.yaml', '-tracking.yaml')
    logging.info('Writing build numbers to track to %s...', tracking_output_filename)
    with open(tracking_output_filename, 'w', encoding='utf-8') as output_file:
        yaml.dump(build_jobs_dict, output_file)
    if len(jobs_info_dict[FAILED_JOBS]) > 0:
        logging.debug('Failed builds: %s', jobs_info_dict[FAILED_JOBS])
        delete_count = 0
        for successful_job in jobs_info_dict[SUCCESSFUL_JOBS]:
            del remaining_builds_dict[BUILD][HOSTS][build_host_index]['jobs'][(
                    successful_job['index'] - delete_count)
            ]
            delete_count += 1
        output_file_name = build_jobs_yaml.replace('.yaml', '-remaining.yaml')
        logging.info('Outputting remaining (failed) jobs to %s...', output_file_name)
        with open(output_file_name, 'w', encoding='utf-8') as output_file:
            yaml.dump(remaining_builds_dict, output_file)


@jenkins_commands.command()
@verbose_option
@job_name_option
@build_number_option
def get_console_output(verbose: bool, job_name: str, build_number: int) -> None:
    """Gets console output for specific Jenkins job build"""
    load_dotenv()
    initialize_logging(verbose)
    logging.info('Getting console output for (%s) build number #%s...',
                 job_name,
                 build_number)
    console_output = get_jenkins_console_output(
        JenkinsRequestSettings(
            os.getenv(JENKINS_URL),
            (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)),
            1),
        job_name, build_number)
    logging.info('Console output: \n%s', console_output)


@jenkins_commands.command()
@verbose_option
@job_name_option
@build_number_option
def get_jenkins_json(verbose: bool, job_name: str, build_number: int) -> None:
    """Gets Jenkins job build JSON data from REST API"""
    load_dotenv()
    initialize_logging(verbose)
    logging.info('Getting API JSON for (%s) build number #%s...',
                 job_name,
                 build_number)
    jenkins_dict = get_jenkins_job_dict(
        JenkinsRequestSettings(
            os.getenv(JENKINS_URL),
            (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)),
            1),
        job_name, build_number)
    logging.info('Jenkins JSON: \n%s', jenkins_dict)


@jenkins_commands.command()
@verbose_option
@url_end_option
@build_number_option
def get_jenkins_job_status(verbose: bool, url_end: str, build_number: int) -> None:
    """Gets jenkins job status"""
    load_dotenv()
    initialize_logging(verbose)
    url_end = trim_url_end_option_util(url_end)
    logging.info('Getting job status for (%s) build number #%s...', url_end, build_number)
    job_status = get_jenkins_job_result_status(
        JenkinsRequestSettings(
            os.getenv(JENKINS_URL),
            (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)),
            1),
        url_end,
        build_number)
    logging.info('Jenkins job (%s) build number #%s status: %s',
                 url_end,
                 build_number,
                 job_status)


@jenkins_commands.command()
@verbose_option
@build_jobs_tracking_yaml_file_option
def track_build_jobs_status(verbose: bool, build_jobs_tracking_yaml: str):
    """Tracks build job status"""
    load_dotenv()
    initialize_logging(verbose)
    logging.info('Validating tracking build jobs YAML: %s...', build_jobs_tracking_yaml)
    validation_errors = validate_jenkins_job_build_tracking_yaml(build_jobs_tracking_yaml)
    if len(validation_errors) > 0:
        logging.error(
            'Invalid build jobs tracking YAML: %s, Validation errors:',
            build_jobs_tracking_yaml)
        for validation_error in validation_errors:
            logging.error('Validation Failed for: field: %s -> %s',
                          validation_error.field,
                          validation_error.message)
        sys.exit(1)
    logging.info('Successfully validated tracking builds jobs YAML: %s!', build_jobs_tracking_yaml)
    with open(build_jobs_tracking_yaml, 'r', encoding='utf-8') as build_jobs_tracking_file:
        build_jobs_tracking_dict = yaml.safe_load(build_jobs_tracking_file)
        logging.info('Tracking builds asynchronously...')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(track_multiple_build_job_statuses(build_jobs_tracking_dict))
        loop.close()
    with open(build_jobs_tracking_yaml, 'w', encoding='utf-8') as build_jobs_tracking_file:
        yaml.dump(build_jobs_tracking_dict, build_jobs_tracking_file)
    logging.info('Wrote statuses to %s', build_jobs_tracking_yaml)
