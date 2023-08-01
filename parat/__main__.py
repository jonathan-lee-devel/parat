import click

from parat.cli.jenkins.commands import jenkins_commands
from parat.cli.release_train.commands import release_train_commands

# noinspection PyTypeChecker
cli = click.CommandCollection(sources=[release_train_commands, jenkins_commands])

if __name__ == '__main__':
    cli()
