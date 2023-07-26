import click


def verbose_option(func):
    """A decorator for the verbose command line argument"""
    return click.option('-v', '--verbose', type=click.BOOL, is_flag=True, required=False,
                        help='Increase output verbosity')(func)
