# PatchEvergreen MCP Server

This is a Model Context Protocol (MCP) server that interfaces with the PatchEvergreen API to fetch issues for libraries. It uses FastMCP for proper MCP implementation.

## Setup

1. Install the required dependencies:
```bash
pip3 install -r requirements.txt
```

2. Create a `.env` file (optional) to configure the server:
```bash
PORT=8080  # Default port is 8080
```

## Running the Server

Start the server with:
```bash
python3 mcp_server.py
```

The server will start on `http://localhost:8080` by default.

## MCP Endpoint

The server implements the Model Context Protocol (MCP) standard using FastMCP. It automatically handles all MCP-specific communication, including streaming responses.

**Example Request:**
```bash
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "get issues for library example in en"
      }
    ]
  }'
```

**Example Response:**
```json
{
    "messages": [
        {
            "role": "assistant",
            "content": "{\"status\":\"success\",\"data\":[...]}"
        }
    ]
}
```

## Error Handling

The server will return appropriate error messages if:
- No user message is found in the request
- The library and language parameters cannot be parsed from the message
- The PatchEvergreen API request fails
- Any other unexpected errors occur

All responses are handled automatically by FastMCP, including proper streaming and error handling.