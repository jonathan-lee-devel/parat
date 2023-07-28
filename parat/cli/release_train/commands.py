import json
import logging
import click

from parat.cli.options import verbose_option, release_specifier_option, input_file_option
from parat.utils.logging_utils import initialize_logging

# JSON file keys
RELEASE = 'release'
APP_GROUPS = 'app-groups'
ICCP = 'iccp'
VERSION = 'version'
PURCHASE_CONTROL_BATCH = 'purchasecontrol_batch'
PURCHASE_CONTROL_BATCH_NGFT = 'purchasecontrol_batch_ngft'
SD_COM_API = 'sdCommercialAPIWeb_ComAPI'
SD_COM_API_BATCH = 'sdCommercialAPIWeb_ComAPIBatch'
SD_COM_API_REPORT = 'sdCommercialAPIWeb_ComAPIReport'
SD_PURCHASE_CONTROL_WEB = 'sdPurchaseControlWeb'


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
        json_file.close()
        iccp = content[RELEASE][APP_GROUPS][release_specifier][ICCP]
        logging.info(f'Opening and parsing {input_file}')
        iccp[PURCHASE_CONTROL_BATCH][VERSION] = '1.2.3'
        iccp[PURCHASE_CONTROL_BATCH_NGFT][VERSION] = '1.2.3'
        iccp[SD_COM_API][VERSION] = '1.2.3'
        iccp[SD_COM_API_BATCH][VERSION] = '1.2.3'
        iccp[SD_COM_API_REPORT][VERSION] = '1.2.3'
        iccp[SD_PURCHASE_CONTROL_WEB][VERSION] = '1.2.3'
        logging.info(f'Writing updated contents to {input_file}')
        json_file = open(input_file, 'w')
        json_file.write(json.dumps(content, indent=2))
        json_file.close()
    except FileNotFoundError:
        logging.error(f'File: {input_file} does not exist')
    except KeyError:
        logging.error(f'Key: {release_specifier} does not exist in {input_file}')


