"""
bds-cli - Minecraft Bedrock Script API CLI Tool

A CLI for managing Minecraft Bedrock scripting projects.
"""

import click

from src.commands.init import run_init
from src.commands.add import run_add


@click.group()
@click.version_option(version="0.1.0", prog_name="bds-cli")
def cli():
    """bds-cli - Minecraft Bedrock Script API Manager"""
    pass


@cli.command()
@click.argument("directory", default=".", type=click.Path())
def init(directory: str):
    """
    Initialize a new Minecraft Bedrock script project.

    Creates a manifest.json file in the specified DIRECTORY (defaults to current directory).
    """
    run_init(directory)


@cli.command()
@click.argument("script_name")
@click.option(
    "-d", "--directory",
    default=".",
    type=click.Path(),
    help="Project directory (defaults to current directory)"
)
def add(script_name: str, directory: str):
    """
    Add a script package from the registry.

    Downloads SCRIPT_NAME from the registry and adds it to scripts/lib/.
    """
    run_add(script_name, directory)


if __name__ == "__main__":
    cli()
