---
name: PatchEvergreen
description: MCP server for accessing PatchEvergreen's breaking changes database. Fetches breaking changes and compatibility issues between versions of programming libraries across multiple languages.
---

# PatchEvergreen Skill

This skill allows you to check for breaking changes, deprecated features, and compatibility issues for libraries across multiple ecosystems.

## Tools

### get_issues_for_library
Fetch breaking changes and compatibility issues for a specific library and programming language.

**Parameters:**
- `library` (string): The name of the library/package (e.g., 'requests', 'lodash', 'django', 'express', 'phpmailer/phpmailer')
- `language` (string): The programming language of the library (e.g., 'python', 'javascript', 'java', 'ruby', 'php', 'go')

```bash
curl -s -G "https://app.patchevergreen.com/api/getissuesforlibrary.php" \
  --data-urlencode "library=$library" \
  --data-urlencode "language=$language"
```

## Usage Instructions

Use this skill when a user asks about library upgrades, breaking changes, or dependency audits.

### Analyzing Breaking Changes
When asked to analyze breaking changes for a library:
1. Use `get_issues_for_library` to fetch the data.
2. Provide a summary of critical breaking changes.
3. Assess the version impact.
4. Rank changes by priority/severity.
5. Provide code examples (before/after) where possible.

### Dependency Audit
When performing a dependency audit:
1. List all dependencies and their current versions.
2. For each dependency, use `get_issues_for_library` to check for issues.
3. Classify impacts as High, Medium, or Low.
4. Recommend an update strategy and timeline.

### Version Upgrade Planning
When planning an upgrade from one version to another:
1. Identify all breaking changes between the current and target versions.
2. Determine if an incremental upgrade is safer.
3. Map changes to specific code impact areas.
4. Define a testing and rollback strategy.

### Compatibility Impact Summary
When a concise summary is needed:
1. Focus on API breaking changes (signatures, removals).
2. Note configuration and behavioral changes.
3. Assess the overall migration effort.
