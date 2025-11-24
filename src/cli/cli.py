import click

from cli.commands.day import day
from cli.commands.new_year import new_year


@click.group
def cli() -> None:
    pass


def setup() -> None:
    cli.add_command(day)
    cli.add_command(new_year)
    cli(obj={})
