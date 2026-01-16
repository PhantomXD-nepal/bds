import json
import uuid
import requests


def get_latest_npm_version(package_name: str) -> str:
    """Fetch the latest version of an npm package from the registry."""
    response = requests.get(f"https://registry.npmjs.org/{package_name}", timeout=10)
    response.raise_for_status()
    return response.json()["dist-tags"]["latest"]


def generate_uuid() -> str:
    """Generate a random UUID string."""
    return str(uuid.uuid4())


def generate_manifest(
    name: str,
    description: str,
    dependencies: list[dict],
) -> dict:
    """
    Generate a Minecraft Bedrock manifest.json structure.

    Args:
        name: Project name
        description: Project description
        dependencies: List of dependency dicts with 'module_name' and 'version' keys

    Returns:
        Complete manifest dictionary ready for JSON serialization
    """
    manifest = {
        "format_version": 2,
        "header": {
            "name": name,
            "description": description,
            "uuid": generate_uuid(),
            "version": [1, 0, 0],
            "min_engine_version": [1, 21, 80]
        },
        "modules": [
            {
                "description": "Script resources",
                "language": "javascript",
                "type": "script",
                "uuid": generate_uuid(),
                "version": [1, 0, 0],
                "entry": "scripts/main.js"
            }
        ],
        "dependencies": dependencies
    }

    return manifest


def write_manifest(manifest: dict, path: str) -> None:
    """Write manifest dictionary to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
