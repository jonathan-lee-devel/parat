"""Jenkins REST API CLI commands module"""
import logging
import os
from http import HTTPStatus

import click
from dotenv import load_dotenv

from parat.cli.common.options import verbose_option
from parat.cli.jenkins.basic.options import (
    job_name_option, build_number_option, url_end_option,
    trim_url_end_option_util
)
from parat.constants.jenkins_env import JENKINS_URL, JENKINS_USER, JENKINS_TOKEN
from parat.use_cases.jenkins_job_info import get_jenkins_job_result_status
from parat.utils.jenkins_rest_api.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins_rest_api.jenkins_utils import (
    get_jenkins_console_output, get_jenkins_job_dict,
    start_jenkins_build,
    start_jenkins_build_url_end
)
from parat.utils.logging_utils import initialize_logging


@click.group(name='jenkins_basic_commands')
def jenkins_basic_commands() -> None:
    """Entry point"""


@jenkins_basic_commands.command()
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


@jenkins_basic_commands.command()
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


@jenkins_basic_commands.command()
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


@jenkins_basic_commands.command()
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


@jenkins_basic_commands.command()
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
