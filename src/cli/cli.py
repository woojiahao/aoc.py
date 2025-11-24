import click

from cli.commands.day import day


@click.group
def cli() -> None:
    pass


def setup() -> None:
    cli.add_command(day)
    cli(obj={})
