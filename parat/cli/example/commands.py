import logging
import click

from parat.cli.options import verbose_option
from parat.utils.logging_utils import initialize_logging


@click.group(name='example')
def example_commands() -> None:
    """Entry point"""
    pass


@example_commands.command()
@verbose_option
def example_command(verbose: bool) -> None:
    initialize_logging(verbose)
    logging.info('Example output')
    logging.debug('Verbose output only')
