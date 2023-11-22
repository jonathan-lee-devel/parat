import click

from parat.cli.jenkins.commands import jenkins_commands

# noinspection PyTypeChecker
cli = click.CommandCollection(sources=[jenkins_commands])

if __name__ == '__main__':
    cli()
