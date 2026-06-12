from flask import Flask, Response, jsonify
from pathlib import Path

# Initialize Flask app for serving Skill file
app = Flask(__name__)

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
SKILL_FILE = SCRIPT_DIR / "SKILL.md"


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


if __name__ == "__main__":
    # Run Flask server on port 8002
    PORT = 8002
    print(f"Starting Flask server on port {PORT}...")
    print("Serving Skill endpoints:")
    print(f"  - Skill file: http://localhost:{PORT}/.well-known/skill")
    print(f"  - Skill metadata: http://localhost:{PORT}/.well-known/skill/metadata")
    print(f"  - Skills list: http://localhost:{PORT}/.well-known/skills")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False, threaded=True)
