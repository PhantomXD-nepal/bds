"""
Add command for bds-cli.

Downloads scripts from the registry and adds them to scripts/lib folder.
"""

import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path

import click
import requests

# Path to the registry file (relative to the package)
REGISTRY_PATH = Path(__file__).parent.parent.parent / "registry.json"


def load_registry() -> dict:
    """Load the package registry from registry.json."""
    if not REGISTRY_PATH.exists():
        click.echo(click.style("Error: registry.json not found", fg="red"))
        return {"packages": {}}

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def download_github_repo(github_url: str, target_dir: Path) -> bool:
    """
    Download a GitHub repository as a zip and extract it to target_dir.

    Args:
        github_url: GitHub repository URL (e.g., https://github.com/user/repo)
        target_dir: Directory to extract the repository contents to

    Returns:
        True if successful, False otherwise
    """
    # Convert GitHub URL to zip download URL (main branch)
    # https://github.com/user/repo -> https://github.com/user/repo/archive/refs/heads/main.zip
    if github_url.endswith("/"):
        github_url = github_url[:-1]

    zip_url = f"{github_url}/archive/refs/heads/main.zip"

    try:
        click.echo(f"  Downloading from {github_url}...")
        response = requests.get(zip_url, timeout=60, stream=True)
        response.raise_for_status()

        # Create a temporary file to store the zip
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_path = tmp_file.name

        # Extract the zip file
        click.echo("  Extracting...")
        with zipfile.ZipFile(tmp_path, "r") as zip_ref:
            # Get the root folder name in the zip (usually repo-main)
            root_folder = zip_ref.namelist()[0].split("/")[0]

            # Extract to a temp directory first
            with tempfile.TemporaryDirectory() as tmp_extract_dir:
                zip_ref.extractall(tmp_extract_dir)

                # Move contents from extracted folder to target
                extracted_path = Path(tmp_extract_dir) / root_folder

                # Copy all files from extracted folder to target
                if extracted_path.exists():
                    target_dir.mkdir(parents=True, exist_ok=True)
                    for item in extracted_path.iterdir():
                        dest = target_dir / item.name
                        if item.is_dir():
                            if dest.exists():
                                shutil.rmtree(dest)
                            shutil.copytree(item, dest)
                        else:
                            shutil.copy2(item, dest)

        # Clean up temp zip file
        os.unlink(tmp_path)

        return True

    except requests.RequestException as e:
        click.echo(click.style(f"  Failed to download: {e}", fg="red"))
        return False
    except zipfile.BadZipFile:
        click.echo(click.style("  Failed: Invalid zip file", fg="red"))
        return False
    except Exception as e:
        click.echo(click.style(f"  Failed: {e}", fg="red"))
        return False


def run_add(script_name: str, directory: str) -> None:
    """
    Add a script package from the registry.

    Args:
        script_name: Name of the script package to add
        directory: Project directory containing scripts/lib
    """
    project_path = Path(directory).resolve()
    lib_path = project_path / "scripts" / "lib"

    # Check if manifest.json exists (project is initialized)
    manifest_path = project_path / "manifest.json"
    if not manifest_path.exists():
        click.echo(click.style("Error: No manifest.json found. Run 'bds-cli init .' first.", fg="red"))
        return

    # Load registry
    registry = load_registry()
    packages = registry.get("packages", {})

    if script_name not in packages:
        click.echo(click.style(f"Error: Package '{script_name}' not found in registry.", fg="red"))
        click.echo()
        click.echo("Available packages:")
        for pkg_name, pkg_info in packages.items():
            desc = pkg_info.get("description", "No description")
            click.echo(f"  • {pkg_name}: {desc}")
        return

    package_info = packages[script_name]
    github_url = package_info.get("github")

    if not github_url:
        click.echo(click.style(f"Error: No GitHub URL for package '{script_name}'", fg="red"))
        return

    click.echo()
    click.echo(click.style(f"📦 Adding {script_name}...", fg="cyan", bold=True))

    # Target directory for this package
    package_target = lib_path / script_name

    # Download and extract
    success = download_github_repo(github_url, package_target)

    if success:
        click.echo()
        click.echo(click.style(f"✓ Added {script_name} to scripts/lib/", fg="green", bold=True))
        click.echo(f"  Location: {package_target}")
    else:
        click.echo()
        click.echo(click.style(f"✗ Failed to add {script_name}", fg="red", bold=True))
