import click

from parat.cli.example.commands import example_commands
from parat.cli.release_train.commands import release_train_commands

# noinspection PyTypeChecker
cli = click.CommandCollection(sources=[example_commands, release_train_commands])

if __name__ == '__main__':
    cli()
