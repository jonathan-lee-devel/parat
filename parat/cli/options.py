import click


def verbose_option(func):
    """A decorator for the verbose command line argument"""
    return click.option('-v', '--verbose', type=click.BOOL, is_flag=True, required=False,
                        help='Increase output verbosity')(func)


def input_file_option(func):
    """A decorator for the input file command line argument"""
    return click.option('-if', '--input-file', type=click.STRING, is_flag=False, required=True,
                        help='Input file path')(func)


def release_specifier_option(func):
    """A decorator for the release specifier command line argument"""
    return click.option('-rs', '--release-specifier', type=click.STRING, is_flag=False, required=True,
                        help='Release specifier')(func)


def job_name_option(func):
    """A decorator for the job name command line argument"""
    return click.option('-jn', '--job-name', type=click.STRING, is_flag=False, required=True,
                        help='Job name')(func)
