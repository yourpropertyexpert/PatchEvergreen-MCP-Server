# PatchEvergreen MCP Server

This is a Model Context Protocol (MCP) server that interfaces with the PatchEvergreen API to fetch issues for breaking changes for libraries. It uses FastMCP for proper MCP implementation.

Please note that libraries are named as written in their respective ecosystem tools, so as you would type them in files like:

- composer.json (php)
- requirements.txt (python)
- manifest.json (Javascript)
- gemfile (Ruby)
- package.json (Javascript)
- cargo.toml (Rust)
- libs.versions.toml (Java)
- pom.xml (Java)
- build.gradle.kts (Kotlin)

## Setup

This is a stdio server that assumes you have a working copy of Python 3 installed on your machine.

Install the required dependencies:
```bash
pip3 install -r requirements.txt
```
[If you are using tools like venv or Docker to run Python, you will need to configure them in your normal way.]


## Using with Cursor

Once installed, this server is designed to be used as a stdio MCP server, typically launched and managed by the Cursor editor. You do not need to run it manually or specify a port.

![MCP.png](./MCP.png)

Cursor automatically communicates with this MCP server over stdio when you invoke MCP features (such as asking for issues for a library) within the editor. No manual requests or HTTP endpoints are needed.

### Configuring MCP Server with .cursor/mcp.json

To configure Cursor to use this MCP server, add a `.cursor/mcp.json` file to your project root with the following content.

```json
{
  "mcpServers": {
    "python-mcp-server": {
      "command": "python3",
      "args": ["/{path_to_this_repo}/mcp_server.py"],
      "env": {}
    }
  }
}
```

- `mcpServers`: A mapping of server names to their configuration.
- `python-mcp-server`: The name for this MCP server configuration (you can choose any name).
- `command`: The executable to launch the server (here, `python3`).
- `args`: Arguments to pass to the command (the path to your `mcp_server.py`).
- `env`: (Optional) Environment variables to set when launching the server.

Once this file is in place, Cursor will automatically launch and manage the MCP server as needed. Simply use MCP features in Cursor, and all communication and error handling will be managed automatically.

## MCP Endpoint

The server implements the Model Context Protocol (MCP) standard using FastMCP. It automatically handles all MCP-specific communication, including streaming responses.

## Error Handling

The server will return appropriate error messages if:
- No user message is found in the request
- The library and language parameters cannot be parsed from the message
- The PatchEvergreen API request fails
- Any other unexpected errors occur

All responses are handled automatically by FastMCP, including proper streaming and error handling.
