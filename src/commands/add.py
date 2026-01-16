"""
Add command for bds.

Downloads scripts from the registry and adds them to scripts/lib folder.
"""

import json
import os
import shutil
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


def parse_github_url(github_url: str) -> tuple[str, str, str, str]:
    """
    Parse a GitHub URL to extract owner, repo, branch, and path.

    Handles URLs like:
    - https://github.com/owner/repo/tree/main/path/to/folder
    - https://github.com/owner/repo

    Returns:
        Tuple of (owner, repo, branch, path)
    """
    # Remove trailing slash
    github_url = github_url.rstrip("/")

    # Remove https://github.com/
    path_part = github_url.replace("https://github.com/", "")

    parts = path_part.split("/")

    owner = parts[0]
    repo = parts[1]

    # Check if there's a tree/branch/path structure
    if len(parts) > 2 and parts[2] == "tree":
        branch = parts[3]
        subpath = "/".join(parts[4:]) if len(parts) > 4 else ""
    else:
        branch = "main"
        subpath = ""

    return owner, repo, branch, subpath


def download_github_folder(
    owner: str, repo: str, branch: str, folder_path: str, target_dir: Path
) -> bool:
    """
    Download a folder from GitHub using the Contents API.

    Args:
        owner: Repository owner
        repo: Repository name
        branch: Branch name
        folder_path: Path to folder within the repo
        target_dir: Local directory to download to

    Returns:
        True if successful, False otherwise
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_path}"
    if branch:
        api_url += f"?ref={branch}"

    try:
        click.echo(f"  Fetching contents from {owner}/{repo}...")
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()

        contents = response.json()

        if not isinstance(contents, list):
            # Single file, not a directory
            contents = [contents]

        target_dir.mkdir(parents=True, exist_ok=True)

        for item in contents:
            item_name = item["name"]
            item_type = item["type"]
            item_path = item["path"]

            if item_type == "file":
                # Download the file
                download_url = item["download_url"]
                click.echo(f"    Downloading {item_name}...")

                file_response = requests.get(download_url, timeout=30)
                file_response.raise_for_status()

                file_path = target_dir / item_name
                file_path.write_bytes(file_response.content)

            elif item_type == "dir":
                # Recursively download subdirectory
                subdir_path = target_dir / item_name
                click.echo(f"    Entering {item_name}/...")
                success = download_github_folder(
                    owner, repo, branch, item_path, subdir_path
                )
                if not success:
                    return False

        return True

    except requests.RequestException as e:
        click.echo(click.style(f"  Failed to download: {e}", fg="red"))
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
        click.echo(
            click.style(
                "Error: No manifest.json found. Run 'bds init .' first.", fg="red"
            )
        )
        return

    # Load registry
    registry = load_registry()
    packages = registry.get("packages", {})

    if script_name not in packages:
        click.echo(
            click.style(f"Error: Package '{script_name}' not found in registry.", fg="red")
        )
        click.echo()
        click.echo("Available packages:")
        for pkg_name, pkg_info in packages.items():
            desc = pkg_info.get("description", "No description")
            click.echo(f"  - {pkg_name}: {desc}")
        return

    package_info = packages[script_name]
    github_url = package_info.get("github")

    if not github_url:
        click.echo(
            click.style(f"Error: No GitHub URL for package '{script_name}'", fg="red")
        )
        return

    click.echo()
    click.echo(click.style(f"Adding {script_name}...", fg="cyan", bold=True))

    # Parse the GitHub URL
    owner, repo, branch, folder_path = parse_github_url(github_url)

    click.echo(f"  Repository: {owner}/{repo}")
    click.echo(f"  Branch: {branch}")
    if folder_path:
        click.echo(f"  Path: {folder_path}")

    # Target directory for this package
    package_target = lib_path / script_name

    # Remove existing package if it exists
    if package_target.exists():
        shutil.rmtree(package_target)

    # Download the folder
    success = download_github_folder(owner, repo, branch, folder_path, package_target)

    if success:
        click.echo()
        click.echo(
            click.style(f"Added {script_name} to scripts/lib/", fg="green", bold=True)
        )
        click.echo(f"  Location: {package_target}")
    else:
        click.echo()
        click.echo(click.style(f"Failed to add {script_name}", fg="red", bold=True))
