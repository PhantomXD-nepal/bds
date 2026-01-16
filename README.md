# bds - Bedrock Scripting CLI

A CLI tool for managing Minecraft Bedrock scripting projects.

## Installation

```bash
pip install bds-mcbe
```

## Usage

### Initialize a new project

```bash
bds init .
```

This will interactively prompt you for:
- Project name
- Description
- Dependencies (@minecraft/server, @minecraft/server-ui, etc.)

### List available packages

```bash
bds list
```

### Add a script package

```bash
bds add <package-name>
```

Downloads the package from the registry and adds it to `scripts/lib/`.

## Commands

| Command | Description |
|---------|-------------|
| `bds init [directory]` | Initialize a new Bedrock script project |
| `bds list` | List all available packages in the registry |
| `bds add <package>` | Add a script package to your project |

## License

MIT
