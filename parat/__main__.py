import click

from parat.cli.example.commands import example_commands

# noinspection PyTypeChecker
cli = click.CommandCollection(sources=[example_commands])

if __name__ == '__main__':
    cli()
