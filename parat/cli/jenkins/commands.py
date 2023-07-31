import logging
import os
import yaml

import click
from dotenv import load_dotenv

from parat.cli.options import verbose_option, job_name_option, build_number_option, url_end_option, \
    build_jobs_yaml_file_option
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins.jenkins_utils import get_jenkins_console_output, get_jenkins_job_dict, start_jenkins_build, \
    start_jenkins_build_url_end
from parat.utils.logging_utils import initialize_logging


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
        JenkinsRequestSettings(os.getenv('JENKINS_URL'), (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1),
        job_name).status_code
    if response_status_code == 201:
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
        JenkinsRequestSettings(os.getenv('JENKINS_URL'), (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1),
        url_end)
    if response_status_code == 201:
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
        print(remaining_builds_dict)
        for build_host_index in range(len(build_jobs_dict['build']['hosts'])):
            build_host = build_jobs_dict['build']['hosts'][build_host_index]
            for build_job_index in range(len(build_host['jobs'])):
                build_job_url_end = build_host['jobs'][build_job_index]
                response_status_code = start_jenkins_build_url_end(
                    JenkinsRequestSettings(build_host['url'], (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')),
                                           1), build_job_url_end)
                if response_status_code == 201:
                    logging.info(f'Successfully kicked off build [{build_host["url"]}] ({build_job_url_end})!')
                    successful_jobs.append({'url': build_host['url'], 'end': build_job_url_end, 'index': build_job_index})
                else:
                    logging.error(f'Failed to kick off build [{build_host["url"]}] ({build_job_url_end}!')
                    failed_jobs.append({'url': build_host['url'], 'end': build_job_url_end, 'index': build_job_index})
    logging.info('============================================================')
    logging.info(f'Run of {build_jobs_yaml} completed:')
    logging.info(f'Successful builds: {successful_jobs}')
    if len(failed_jobs) > 0:
        logging.error(f'Failed builds: {failed_jobs}')
        delete_count = 0
        for successful_job in successful_jobs:
            del remaining_builds_dict['build']['hosts'][build_host_index]['jobs'][successful_job['index'] - delete_count]
            delete_count += 1
        logging.info(f'')
        output_file_name = build_jobs_yaml.replace('.yaml', '-output.yaml')
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
        JenkinsRequestSettings(os.getenv('JENKINS_URL'), (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1),
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
        JenkinsRequestSettings(os.getenv('JENKINS_URL'), (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1),
        job_name, build_number)
    logging.info(f'Jenkins JSON: \n{jenkins_dict}')
