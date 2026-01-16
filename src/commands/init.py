"""
Init command for bds-cli.

Creates a manifest.json file with interactive prompts for project configuration.
"""

import os
from pathlib import Path

import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from src.utils.manifetGen import (
    generate_manifest,
    get_latest_npm_version,
    write_manifest,
)

# Available Minecraft scripting API dependencies
AVAILABLE_DEPENDENCIES = [
    "@minecraft/server",
    "@minecraft/server-ui",
    "@minecraft/server-net",
    "@minecraft/server-admin",
]


def fetch_dependency_versions(selected_deps: list[str]) -> list[dict]:
    """
    Fetch latest versions for selected dependencies from npm registry.

    Args:
        selected_deps: List of package names to fetch versions for

    Returns:
        List of dependency dicts with 'module_name' and 'version' keys
    """
    dependencies = []

    for dep in selected_deps:
        click.echo(f"  Fetching {dep}...", nl=False)
        try:
            version = get_latest_npm_version(dep)
            click.echo(f" {version}")
            dependencies.append({"module_name": dep, "version": version})
        except Exception as e:
            click.echo(click.style(f" Failed: {e}", fg="red"))

    return dependencies


def run_init(directory: str) -> None:
    """
    Run the interactive init process.

    Args:
        directory: Target directory for manifest.json
    """
    target_path = Path(directory).resolve()
    manifest_path = target_path / "manifest.json"

    # Check if manifest already exists
    if manifest_path.exists():
        overwrite = inquirer.confirm(
            message="manifest.json already exists. Overwrite?", default=False
        ).execute()

        if not overwrite:
            click.echo("Aborted.")
            return

    click.echo()
    click.echo(
        click.style(
            "🎮 bds-cli - Minecraft Bedrock Script Project", fg="cyan", bold=True
        )
    )
    click.echo()

    # Prompt for project name
    name = inquirer.text(
        message="Project name:",
        validate=lambda x: len(x.strip()) > 0,
        invalid_message="Project name cannot be empty",
    ).execute()

    # Prompt for description
    description = inquirer.text(
        message="Description:",
        validate=lambda x: len(x.strip()) > 0,
        invalid_message="Description cannot be empty",
    ).execute()

    # Prompt for dependencies (multi-select checkbox)
    selected_deps = inquirer.checkbox(
        message="Select dependencies:",
        choices=[Choice(dep, name=dep) for dep in AVAILABLE_DEPENDENCIES],
        instruction="(Use ↑↓ to move, Space to select, Enter to confirm)",
    ).execute()

    click.echo()

    # Fetch versions for selected dependencies
    dependencies = []
    if selected_deps:
        click.echo(click.style("Fetching latest versions...", fg="yellow"))
        dependencies = fetch_dependency_versions(selected_deps)
        click.echo()

    # Generate and write manifest
    manifest = generate_manifest(
        name=name.strip(),
        description=description.strip(),
        dependencies=dependencies,
    )

    # Ensure target directory exists
    target_path.mkdir(parents=True, exist_ok=True)

    write_manifest(manifest, str(manifest_path))

    click.echo(click.style("✓ Created manifest.json", fg="green", bold=True))
    click.echo(f"  Location: {manifest_path}")

    click.echo("Creating the necessary folders.")
    # Create a new scripts folder with a main.js file
    scripts_dir_path = target_path / "scripts"
    main_js_path = scripts_dir_path / "main.js"

    scripts_dir_path.mkdir(exist_ok=True)

    if not main_js_path.exists():
        main_js_path.write_text(
            "// Entry point for your Bedrock Script\n"
            "import { world } from '@minecraft/server';\n\n"
            "world.sendMessage('Hello from bds-cli!');\n"
        )

    click.echo(click.style("Created scripts/main.js", fg="green"))
