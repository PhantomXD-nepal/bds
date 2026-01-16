This is a CLI tool like pnpm but instead of managing javascript dependencies, it manages mcpe scripting api's scripts.This may seem vague but here is a brief
description of what it does:
- Install, update, and remove scripts
- Manage dependencies between scripts
- Run scripts with ease



bds-cli init .

creates a manifest.json file template to refer to as
```
{
  "format_version": 2,
  "header": {
    "name": "CustomCommands",
    "description": "TypeScript Starter",
    "uuid": "490cb58c-e6b1-4af2-8f48-433b96ae8dcd",
    "version": [1, 0, 0],
    "min_engine_version": [1, 21, 80]
  },
  "modules": [
    {
      "description": "Script resources",
      "language": "javascript",
      "type": "script",
      "uuid": "d6cc3ec1-f3d6-4ee1-9883-e01852a27c7a",
      "version": [1, 0, 0],
      "entry": "scripts/main.js"
    }
  ],
  "dependencies": [
    {
      "module_name": "@minecraft/server",
      "version": "2.1.0"
    },
    {
      "uuid": "06f36430-433b-4315-a30f-02d41e54b078",
      "version": [1, 0, 0]
    }
  ]
}
```

upon execution it should ask the user for the following things
- Name of the script
- Descriptions
--- Choosing dependencies 
    @minecraft/server []
    @minecraft/server-ui []
    @minecraft/server-net []
    @minecraft/server-admin []
  
the user should be able to choose dependencies from a list of available dependencies
it should auto fetch the latest version of the dependency from this website
