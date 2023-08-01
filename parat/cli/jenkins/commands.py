import logging
import os
import click
import yaml

from http import HTTPStatus
from dotenv import load_dotenv

from parat.cli.options import verbose_option, job_name_option, build_number_option, url_end_option, \
    build_jobs_yaml_file_option
from parat.constants import BUILD, HOSTS, JENKINS_URL, JENKINS_USER, JENKINS_TOKEN, SUCCESSFUL_JOBS, FAILED_JOBS, END
from parat.use_cases.jenkins_builds import process_build_host
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins.jenkins_utils import get_jenkins_console_output, get_jenkins_job_dict, start_jenkins_build, \
    start_jenkins_build_url_end
from parat.utils.logging_utils import initialize_logging, logging_line_break


@click.group(name='jenkins')
def jenkins_commands() -> None:
    """Entry point"""
    pass


@jenkins_commands.command()
@verbose_option
@job_name_option
def start_build(verbose: bool, job_name: str) -> None:
    load_dotenv()
    initialize_logging(verbose)
    logging.info(f'Kicking off build ({job_name})...')
    response_status_code = start_jenkins_build(
        JenkinsRequestSettings(os.getenv(JENKINS_URL), (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)), 1),
        job_name).status_code
    if response_status_code == HTTPStatus.CREATED:
        logging.info(f'Successfully kicked off build ({job_name})!')
    else:
        logging.error(f'Failed to kick off build ({job_name})!')


@jenkins_commands.command()
@verbose_option
@url_end_option
def start_build_url(verbose: bool, url_end: str) -> None:
    load_dotenv()
    initialize_logging(verbose)
    logging.info(f'Kicking off build ({url_end})...')
    response_status_code = start_jenkins_build_url_end(
        JenkinsRequestSettings(os.getenv(JENKINS_URL), (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)), 1),
        url_end)
    if response_status_code == HTTPStatus.CREATED:
        logging.info(f'Successfully kicked off build ({url_end})!')
    else:
        logging.error(f'Failed to kick off build ({url_end}!')


@jenkins_commands.command()
@verbose_option
@build_jobs_yaml_file_option
def start_build_jobs_yaml(verbose: bool, build_jobs_yaml: str) -> None:
    load_dotenv()
    initialize_logging(verbose)
    logging.info(f'Parsing YAML: {build_jobs_yaml}...')
    successful_jobs = []
    failed_jobs = []
    with open(build_jobs_yaml, 'r') as yaml_file_contents:
        build_jobs_dict = yaml.safe_load(yaml_file_contents)
        remaining_builds_dict = build_jobs_dict
        for build_host_index in range(len(build_jobs_dict[BUILD][HOSTS])):
            build_host = build_jobs_dict[BUILD][HOSTS][build_host_index]
            jobs_info_dict = process_build_host(build_host)
            successful_jobs.append(jobs_info_dict[SUCCESSFUL_JOBS])
            failed_jobs.append(jobs_info_dict[FAILED_JOBS])
    logging_line_break()
    logging.info(f'Run of {build_jobs_yaml} completed:')
    logging.info(f'Successful builds: {jobs_info_dict[SUCCESSFUL_JOBS]}')
    tracking_output_filename = build_jobs_yaml.replace('.yaml', '-tracking-output.yaml')
    logging.info(f'Writing build numbers to track to {tracking_output_filename}...')
    with open(tracking_output_filename, 'w') as output_file:
        yaml.dump(build_jobs_dict, output_file)
    if len(jobs_info_dict[FAILED_JOBS]) > 0:
        logging.error(f'Failed builds: {jobs_info_dict[FAILED_JOBS]}')
        delete_count = 0
        for successful_job in jobs_info_dict[SUCCESSFUL_JOBS]:
            del remaining_builds_dict[BUILD][HOSTS][build_host_index]['jobs'][successful_job['index'] - delete_count]
            delete_count += 1
        output_file_name = build_jobs_yaml.replace('.yaml', '-remaining-output.yaml')
        logging.info(f'Outputting remaining (failed) jobs to {output_file_name}...')
        with open(output_file_name, 'w') as output_file:
            yaml.dump(remaining_builds_dict, output_file)


@jenkins_commands.command()
@verbose_option
@job_name_option
@build_number_option
def get_console_output(verbose: bool, job_name: str, build_number: int) -> None:
    load_dotenv()
    initialize_logging(verbose)
    logging.info(f'Getting console output for ({job_name}) build number #{build_number}...')
    console_output = get_jenkins_console_output(
        JenkinsRequestSettings(os.getenv(JENKINS_URL), (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)), 1),
        job_name, build_number)
    logging.info(f'Console output: \n{console_output}')


@jenkins_commands.command()
@verbose_option
@job_name_option
@build_number_option
def get_jenkins_json(verbose: bool, job_name: str, build_number: int) -> None:
    load_dotenv()
    initialize_logging(verbose)
    logging.info(f'Getting API JSON for ({job_name}) build number #{build_number}...')
    jenkins_dict = get_jenkins_job_dict(
        JenkinsRequestSettings(os.getenv(JENKINS_URL), (os.getenv(JENKINS_USER), os.getenv(JENKINS_TOKEN)), 1),
        job_name, build_number)
    logging.info(f'Jenkins JSON: \n{jenkins_dict}')
