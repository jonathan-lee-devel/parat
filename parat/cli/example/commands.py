import click


@click.group(name='example')
def example_commands() -> None:
    """Entry point"""
    pass
