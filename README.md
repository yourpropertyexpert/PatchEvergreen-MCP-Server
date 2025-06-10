# PatchEvergreen MCP Server

This is a lightweight Model Context Protocol (MCP) server that interfaces with the PatchEvergreen API to fetch issues for breaking changes for libraries. It uses FastMCP for proper MCP implementation. It does not (currently) support API access tokens, so all accesses are "slow" requests into that API.

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

The file mcp_server is a stdio server that assumes you have a working copy of Python 3 installed on your machine.

Install the required dependencies:
```bash
pip3 install -r requirements.txt
```
[If you are using tools like venv or Docker to run Python, you will need to configure them in your normal way.]

## SSE

The file mcp_server_sse is a copy of the stdio file intended for hosting on servers. You probably don't want to do this, but we include it for reference.

To run it, just run python3 mcp_server_sse.py


## Using with Cursor

Once installed, this server is designed to be used as a stdio MCP server, typically launched and managed by the Cursor editor. You do not need to run it manually or specify a port.

![MCP.png](./MCP.png)

Cursor automatically communicates with this MCP server over stdio when you invoke MCP features (such as asking for issues for a library) within the editor. No manual requests or HTTP endpoints are needed.

### Configuring MCP Server with .cursor/mcp.json

To configure Cursor to use this MCP server, add a `.cursor/mcp.json` to your project, with the contents of the mcp.json from this repo.

This will add both the stdio and sse versions of the server. You probably don't want both.

## MCP Endpoint

The server implements the Model Context Protocol (MCP) standard using FastMCP. It automatically handles all MCP-specific communication, including streaming responses.

## Error Handling

The server will return appropriate error messages if:
- No user message is found in the request
- The library and language parameters cannot be parsed from the message
- The PatchEvergreen API request fails
- Any other unexpected errors occur

All responses are handled automatically by FastMCP, including proper streaming and error handling.
