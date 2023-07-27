import json
import logging
import click

from parat.cli.options import verbose_option, release_specifier_option, input_file_option
from parat.utils.logging_utils import initialize_logging


@click.group(name='release-train')
def release_train_commands() -> None:
    """Entry point"""
    pass


@release_train_commands.command()
@verbose_option
@input_file_option
@release_specifier_option
def update_release_train(verbose: bool, input_file: str, release_specifier: str) -> None:
    initialize_logging(verbose)
    try:
        json_file = open(input_file)
        content = json.load(json_file)
        logging.info(content['release']['app-groups'][release_specifier]['iccp'])
    except FileNotFoundError:
        logging.error(f'File: {input_file} does not exist')
    except KeyError:
        logging.error(f'Key: {release_specifier} does not exist in {input_file}')


