import click

from parat.cli.options import verbose_option


@click.group(name='example')
def example_commands() -> None:
    """Entry point"""
    pass


@example_commands.command()
@verbose_option
def example_command(verbose: bool) -> None:
    print('This is an example command...')
    if verbose:
        print('With extra verbose output...')
