"""
List command for bds.

Lists all available packages in the registry.
"""

import json
from pathlib import Path

import click

# Path to the registry file (relative to the package)
REGISTRY_PATH = Path(__file__).parent.parent.parent / "registry.json"


def load_registry() -> dict:
    """Load the package registry from registry.json."""
    if not REGISTRY_PATH.exists():
        return {"packages": {}}

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_list() -> None:
    """List all available packages in the registry."""
    registry = load_registry()
    packages = registry.get("packages", {})

    if not packages:
        click.echo(click.style("No packages available in the registry.", fg="yellow"))
        return

    click.echo()
    click.echo(click.style("Available Packages", fg="cyan", bold=True))
    click.echo(click.style("-" * 50, fg="bright_black"))
    click.echo()

    for pkg_name, pkg_info in packages.items():
        description = pkg_info.get("description", "No description")
        click.echo(f"  {click.style(pkg_name, fg='green', bold=True)}")
        click.echo(f"    {description}")
        click.echo()

    click.echo(click.style("-" * 50, fg="bright_black"))
    click.echo(f"  Total: {len(packages)} package(s)")
    click.echo()
    click.echo("  Use " + click.style("bds add <package-name>", fg="yellow") + " to install a package.")
