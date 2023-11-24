"""Shared/common command line options"""
import click


def verbose_option(func):
    """A decorator for the verbose command line argument"""
    return click.option('-v', '--verbose', type=click.BOOL, is_flag=True, required=False,
                        help='Increase output verbosity')(func)


def input_file_option(func):
    """A decorator for the input file command line argument"""
    return click.option('-if', '--input-file', type=click.STRING, is_flag=False, required=True,
                        help='Input file path')(func)
