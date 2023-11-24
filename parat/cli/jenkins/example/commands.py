"""Commands to demonstrate CLI capabilities"""
import logging
import sys
import click
import yaml
from dotenv import load_dotenv

from parat.cli.common.options import verbose_option
from parat.cli.jenkins.example.options import with_failure_option
from parat.utils.logging_utils import initialize_logging, logging_line_break


@click.group(name='jenkins_example_commands')
def jenkins_example_commands() -> None:
    """Entry point"""


@jenkins_example_commands.command()
@verbose_option
@with_failure_option
def example_output(verbose: bool, with_failure: bool) -> None:
    """Displays example output for Jenkins multi-job run"""
    load_dotenv()
    initialize_logging(verbose)
    logging_line_break()
    logging.info('\n%s', yaml.dump(({
        'jobs': [
            {
                'name': 'TestJob',
                'build': 2,
                'status': 'SUCCESS',
                'url': 'http://localhost:8080/job/TestJob/2'
            }
        ]
    }) if not with_failure else {
        'jobs': [
            {
                'name': 'TestJob',
                'build': 2,
                'status': 'FAILURE',
                'url': 'http://localhost:8080/job/TestJob/2'
            }
        ]
    }))
    logging_line_break()
    if with_failure:
        sys.exit(1)
