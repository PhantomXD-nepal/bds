"""
bds - Bedrock Scripting CLI Tool

A CLI for managing Minecraft Bedrock scripting projects.
"""

import click

from src.commands.add import run_add
from src.commands.init import run_init
from src.commands.list import run_list


@click.group()
@click.version_option(version="0.1.0", prog_name="bds")
def cli():
    """bds - Bedrock Scripting Manager"""
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
    "-d",
    "--directory",
    default=".",
    type=click.Path(),
    help="Project directory (defaults to current directory)",
)
def add(script_name: str, directory: str):
    """
    Add a script package from the registry.

    Downloads SCRIPT_NAME from the registry and adds it to scripts/lib/.
    """
    run_add(script_name, directory)


@cli.command(name="list")
def list_packages():
    """List all available packages in the registry."""
    run_list()


if __name__ == "__main__":
    cli()
