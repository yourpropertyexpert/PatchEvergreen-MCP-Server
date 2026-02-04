from fastmcp import FastMCP
import requests
import os
from flask import Flask, Response, jsonify
from pathlib import Path
import uvicorn
from asgiref.wsgi import WsgiToAsgi

os.environ['HOST'] = '0.0.0.0'

# Initialize Flask app for serving Skill file
app = Flask(__name__)

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
SKILL_FILE = SCRIPT_DIR / "SKILL.md"

# Initialize FastMCP server
mcp = FastMCP(
    name="PatchEvergreen",
    instructions="MCP server for accessing PatchEvergreen's breaking changes database. "
                 "Fetches breaking changes and compatibility issues between versions "
                 "of programming libraries across multiple languages."
)


@mcp.tool()
def get_issues_for_library(library: str, language: str) -> dict:
    """
    Fetch breaking changes and compatibility issues for a specific library and programming language.

    Connects to the PatchEvergreen API to retrieve information about breaking changes,
    deprecated features, and compatibility issues between different versions of libraries.

    Args:
        library (str): The name of the library/package to check for breaking changes as it would appear in a package manager
                      (e.g., 'requests', 'lodash', 'django', 'express', 'phpmailer/phpmailer')
        language (str): The programming language of the library
                       (e.g., 'python', 'javascript', 'java', 'ruby', 'php', 'go')

    Returns:
        dict: Dictionary containing breaking changes information including:
            - issues: List of breaking changes and compatibility issues
            - version information, deprecation notices, migration guidance

    Example:
        get_issues_for_library("phpmailer/phpmailer", "php")
        Returns breaking changes data for the PHP phpmailer library which Packagist would call "phpmailer/phpmailer"
    """
    url = "https://app.patchevergreen.com/api/getissuesforlibrary.php"
    params = {"library": library, "language": language}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


@mcp.prompt()
def analyze_breaking_changes(library: str, language: str) -> str:
    """
    Analyze breaking changes for a library and provide migration guidance.

    This prompt helps users understand the impact of breaking changes in a library
    and provides actionable advice for handling version updates.

    Args:
        library (str): The library name to analyze
        language (str): The programming language

    Returns:
        str: A comprehensive prompt for analyzing breaking changes
    """
    return f"""You are a software engineering expert specializing in library migration and compatibility analysis.

Please analyze the breaking changes for the {language} library "{library}" using the PatchEvergreen database.

Your analysis should include:

1. **Breaking Changes Summary**: List the most critical breaking changes that could affect existing code
2. **Version Impact Assessment**: Identify which version ranges are most affected
3. **Migration Priority**: Rank changes by severity and likelihood of impact
4. **Code Examples**: Where possible, show before/after code examples for major changes
5. **Action Plan**: Provide a step-by-step migration strategy
6. **Testing Recommendations**: Suggest specific areas to focus testing efforts
7. **Timeline Estimation**: Estimate effort required for migration

Focus on practical, actionable advice that developers can immediately use to plan their upgrade strategy.

Use the get_issues_for_library tool to fetch the latest breaking changes data for {library} in {language}."""


@mcp.prompt()
def dependency_audit_report(project_language: str) -> str:
    """
    Generate a comprehensive dependency audit report template.

    This prompt helps create a structured approach to auditing all dependencies
    in a project for breaking changes and security issues.

    Args:
        project_language (str): The primary programming language of the project

    Returns:
        str: A prompt template for conducting dependency audits
    """
    return f"""You are a DevOps and security specialist conducting a comprehensive dependency audit.

Create a detailed dependency audit report for a {project_language} project. For each dependency that the user provides, use the PatchEvergreen database to assess:

## Audit Framework

### 1. Dependency Inventory
- List all direct and indirect dependencies
- Note current versions in use
- Identify outdated packages

### 2. Breaking Changes Analysis
For each dependency, analyze:
- Critical breaking changes since current version
- Deprecation warnings and timelines
- API changes that affect the codebase
- Configuration changes required

### 3. Impact Assessment Matrix
Classify each dependency by:
- **High Impact**: Breaking changes likely to cause failures
- **Medium Impact**: Changes requiring code modifications
- **Low Impact**: Minor changes or documentation updates
- **No Impact**: No breaking changes identified

### 4. Update Strategy
- Prioritized update sequence
- Version pinning recommendations
- Rollback procedures
- Testing requirements for each update

### 5. Timeline and Resource Planning
- Estimated hours per dependency update
- Recommended update batching
- Critical path dependencies
- Team member assignments

Use the get_issues_for_library tool to fetch breaking changes data for each dependency the user wants to audit."""


@mcp.prompt()
def version_upgrade_planner(library: str, language: str, current_version: str, target_version: str) -> str:
    """
    Create a detailed version upgrade plan for a specific library.

    This prompt helps plan a safe upgrade path from one version to another,
    considering all breaking changes along the upgrade path.

    Args:
        library (str): The library to upgrade
        language (str): The programming language
        current_version (str): Current version in use
        target_version (str): Desired target version

    Returns:
        str: A detailed upgrade planning prompt
    """
    return f"""You are a senior software architect planning a critical library upgrade.

Create a comprehensive upgrade plan for {library} ({language}) from version {current_version} to {target_version}.

## Upgrade Planning Framework

### 1. Pre-Upgrade Assessment
- Fetch breaking changes data using get_issues_for_library
- Identify all breaking changes between {current_version} and {target_version}
- Map breaking changes to potential code impact areas
- Assess compatibility with other dependencies

### 2. Incremental Upgrade Strategy
- Determine if direct upgrade is safe or if incremental steps are needed
- Identify stable intermediate versions if step-by-step upgrade is recommended
- Plan upgrade sequence to minimize risk

### 3. Code Impact Analysis
- List specific code patterns that will break
- Identify configuration files that need updates
- Note API changes affecting interfaces
- Highlight performance implications

### 4. Testing Strategy
- Unit tests to update/create
- Integration test scenarios
- Performance benchmarks to run
- Rollback testing procedures

### 5. Implementation Plan
- Detailed step-by-step upgrade process
- Rollback procedures at each step
- Monitoring and validation checkpoints
- Team coordination requirements

### 6. Change Management
- Backup procedures
- Feature flags for gradual rollout
- Monitoring and validation checkpoints
- Emergency rollback triggers

Provide specific, actionable steps that the development team can follow to ensure a safe upgrade process."""


@mcp.prompt()
def compatibility_impact_summary(library: str, language: str) -> str:
    """
    Generate a focused summary of compatibility impacts for a library.

    This prompt helps create concise reports on how breaking changes
    will affect existing codebases and integration patterns.

    Args:
        library (str): The library to analyze
        language (str): The programming language

    Returns:
        str: A compatibility-focused summary prompt
    """
    return f"""You are a software compatibility specialist analyzing library breaking changes.

Create a concise compatibility impact summary for {library} ({language}) using PatchEvergreen data.

## Compatibility Analysis Framework

### 1. API Breaking Changes
- Method signature changes
- Removed or renamed functions/classes
- Parameter requirement changes
- Return type modifications

### 2. Configuration Changes
- Configuration file format changes
- Environment variable modifications
- Default value changes
- Required vs optional parameter changes

### 3. Behavioral Changes
- Different output formats
- Changed error handling patterns
- Modified execution flow
- Performance characteristic changes

### 4. Integration Impact
- Framework compatibility changes
- Plugin/extension compatibility
- Third-party tool integration changes
- Build system requirement changes

### 5. Migration Effort Assessment
- Simple find-and-replace changes
- Logic rewrites required
- Configuration updates needed
- Testing scope implications

### 6. Compatibility Recommendations
- Backward compatibility options
- Gradual migration strategies
- Code organization suggestions
- Version pinning recommendations

Use get_issues_for_library to fetch breaking changes data and focus on practical compatibility concerns that developers need to address."""


# Expose SKILL.md as an MCP resource
@mcp.resource(uri="skill://patch-evergreen/SKILL.md")
def get_skill_resource() -> str:
    """Get the PatchEvergreen Skill file as an MCP resource."""
    if SKILL_FILE.exists():
        with open(SKILL_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise FileNotFoundError("SKILL.md file not found")


# HTTP endpoints for Skill access
@app.route('/.well-known/skill', methods=['GET'])
@app.route('/api/skill', methods=['GET'])
@app.route('/skill', methods=['GET'])
def get_skill():
    """Serve the SKILL.md file for web clients."""
    if SKILL_FILE.exists():
        with open(SKILL_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content, mimetype='text/markdown; charset=utf-8')
    else:
        return jsonify({"error": "Skill file not found"}), 404


@app.route('/.well-known/skill/metadata', methods=['GET'])
@app.route('/api/skill/metadata', methods=['GET'])
def get_skill_metadata():
    """Serve only the YAML frontmatter for skill discovery."""
    if SKILL_FILE.exists():
        with open(SKILL_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter (between --- markers)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                return Response(frontmatter, mimetype='text/yaml; charset=utf-8')

        return jsonify({"error": "Invalid skill format"}), 400
    else:
        return jsonify({"error": "Skill file not found"}), 404


@app.route('/.well-known/skills', methods=['GET'])
@app.route('/api/skills', methods=['GET'])
def list_skills():
    """List available skills (for discovery)."""
    if SKILL_FILE.exists():
        with open(SKILL_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from frontmatter
        metadata = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key == 'tags' and value.startswith('['):
                            # Handle array format
                            metadata[key] = [t.strip().strip('"').strip("'") for t in value.strip('[]').split(',')]
                        else:
                            metadata[key] = value

        return jsonify(
            {
                "skills": [
                    {
                        "name": metadata.get("name", "PatchEvergreen Breaking Changes Analyzer"),
                        "description": metadata.get("description", ""),
                        "version": metadata.get("version", "1.0.0"),
                        "url": "/.well-known/skill",
                    }
                ]
            }
        )
    else:
        return jsonify({"skills": []})


# Add /sse route in Flask as fallback (will be overridden by ASGI router if MCP app works)
@app.route('/sse', methods=['GET', 'POST'])
def sse_endpoint():
    """MCP SSE endpoint - handled by FastMCP if ASGI routing works, otherwise returns info."""
    return jsonify({
        "error": "MCP SSE endpoint",
        "message": "This endpoint should be handled by FastMCP's SSE transport. "
                   "If you see this message, the ASGI routing may not be working correctly.",
        "note": "MCP SSE requires proper ASGI integration. Check server logs for details."
    }), 503


if __name__ == "__main__":
    # Single port solution: Everything on port 8000
    # Using uvicorn with ASGI routing - all in Python, no nginx needed!

    PORT = 8000

    print(f"Starting unified Python server on port {PORT}")
    print("All endpoints available on the same port:")
    print(f"  - MCP SSE: http://localhost:{PORT}/sse")
    print(f"  - Skill file: http://localhost:{PORT}/.well-known/skill")
    print(f"  - Skill metadata: http://localhost:{PORT}/.well-known/skill/metadata")
    print(f"  - Skills list: http://localhost:{PORT}/.well-known/skills")

    # Convert Flask (WSGI) to ASGI so we can run it with uvicorn
    flask_asgi = WsgiToAsgi(app)

    # Get FastMCP's ASGI app for SSE endpoint
    # FastMCP creates an ASGI app internally when using SSE transport
    mcp_asgi_app = None
    try:
        # FastMCP's internal structure - try to access the SSE app
        # The mcp.run() method creates a server, but we want the app before running
        from fastmcp.server.sse import create_sse_app

        # Create the SSE ASGI app directly
        mcp_asgi_app = create_sse_app(mcp)
        print("Successfully created FastMCP SSE app")

    except (ImportError, AttributeError) as e:
        print(f"Warning: Could not import create_sse_app: {e}")
        print("Using Flask-only mode. /sse endpoint will show info message.")

        # Since we can't get FastMCP's SSE app, just use Flask
        # The /sse route in Flask will return an info message
        print(f"\nStarting Flask server on port {PORT}...")
        print("Note: MCP SSE endpoint (/sse) will return info message.")
        print("Skill endpoints will work normally.")
        app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False, threaded=True)
        return  # Exit early

    # If we successfully got the MCP ASGI app, create unified router
    if mcp_asgi_app:
        class UnifiedASGIApp:
            def __init__(self, mcp_app, flask_app):
                self.mcp_app = mcp_app
                self.flask_app = flask_app

            async def __call__(self, scope, receive, send):
                if scope["type"] != "http":
                    await self.flask_app(scope, receive, send)
                    return

                path = scope.get("path", "")

                # Route /sse to MCP, everything else to Flask
                if path == "/sse" or path.startswith("/sse/"):
                    await self.mcp_app(scope, receive, send)
                else:
                    await self.flask_app(scope, receive, send)

        unified_app = UnifiedASGIApp(mcp_asgi_app, flask_asgi)

        print(f"\nStarting unified ASGI server on port {PORT}...")
        print("All routing handled in Python - no nginx needed!")
        uvicorn.run(unified_app, host="0.0.0.0", port=PORT, log_level="info")
    else:
        # Fallback: Just run Flask (MCP SSE won't work, but Skill endpoints will)
        print(f"\nStarting Flask server on port {PORT} (MCP SSE not available)...")
        print("Note: /sse endpoint will return info message. Skill endpoints will work.")
        app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False, threaded=True)
