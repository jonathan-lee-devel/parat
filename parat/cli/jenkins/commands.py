import logging
import os

import click
from dotenv import load_dotenv

from parat.cli.options import verbose_option, job_name_option
from parat.enums.http_request_methods import HttpRequestMethod
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.logging_utils import initialize_logging
from parat.utils.request_retry import request_retry


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
    response_status_code = request_retry(HttpRequestMethod.POST,
                                         f'{os.getenv("JENKINS_URL")}/job/{job_name}/build?delay=0sec',
                                         1,
                                         HttpRequestSettings(None, None, False,
                                                             (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')))
                                         ).status_code
    if response_status_code == 201:
        logging.info('Successfully kicked off build!')
    else:
        logging.error('Failed to kick off build!')


@jenkins_commands.command()
@verbose_option
@job_name_option
def jenkins_command(verbose: bool, job_name: str) -> None:
    load_dotenv()
    initialize_logging(verbose)
    console_output = request_retry(HttpRequestMethod.GET,
                                   f'{os.getenv("JENKINS_URL")}/job/{job_name}/1/logText/progressiveText?start=0',
                                   1,
                                   HttpRequestSettings(None, None, False, (os.getenv('JENKINS_USER'), 'password'))
                                   ).text
    logging.info(f'Console output: \n{console_output}')
    logging.info('Connecting to Jenkins again...')
    jenkins_dict = request_retry(HttpRequestMethod.GET,
                                 f'{os.getenv("JENKINS_URL")}/job/{job_name}/1/api/json',
                                 1,
                                 HttpRequestSettings(None, None, False, (os.getenv('JENKINS_USER'), 'password'))
                                 ).json()
    logging.info(f'Jenkins JSON: \n{jenkins_dict}')
