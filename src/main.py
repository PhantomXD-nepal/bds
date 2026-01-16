"""
bds-cli - Minecraft Bedrock Script API CLI Tool

A CLI for managing Minecraft Bedrock scripting projects.
"""

import click

from src.commands.init import run_init


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


if __name__ == "__main__":
    cli()
