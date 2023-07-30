import logging
import os

import click
from dotenv import load_dotenv

from parat.cli.options import verbose_option, job_name_option, build_number_option
from parat.utils.jenkins.jenkins_utils import get_jenkins_console_output, get_jenkins_job_dict, start_jenkins_build
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
    response_status_code = start_jenkins_build(os.getenv('JENKINS_URL'), (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1, job_name).status_code
    if response_status_code == 201:
        logging.info('Successfully kicked off build!')
    else:
        logging.error('Failed to kick off build!')


@jenkins_commands.command()
@verbose_option
@job_name_option
@build_number_option
def get_console_output(verbose: bool, job_name: str, build_number: int) -> None:
    load_dotenv()
    initialize_logging(verbose)
    logging.info(f'Getting console output for ({job_name}) build number #{build_number}...')
    console_output = get_jenkins_console_output(os.getenv('JENKINS_URL'), (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1, job_name, build_number)
    logging.info(f'Console output: \n{console_output}')


@jenkins_commands.command()
@verbose_option
@job_name_option
@build_number_option
def get_jenkins_json(verbose: bool, job_name: str, build_number: int) -> None:
    load_dotenv()
    initialize_logging(verbose)
    logging.info(f'Getting API JSON for ({job_name}) build number #{build_number}...')
    jenkins_dict = get_jenkins_job_dict(os.getenv('JENKINS_URL'), (os.getenv('JENKINS_USER'), os.getenv('JENKINS_TOKEN')), 1, job_name, build_number)
    logging.info(f'Jenkins JSON: \n{jenkins_dict}')
