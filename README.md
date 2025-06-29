# Doc Finder MCP Server

A Model Context Protocol server that allows you to fetch documentation or coding guidelines stored in a GitHub repository or local filesystem, on demand.


## Installation

Install [uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Configuration

The `uvx` command is provided by uv and allows you to run Python packages directly.

You can configure the server to read from either a GitHub repository or a local filesystem directory.

### GitHub Repository (Public)

If the documentation is stored in a public GitHub repository:

```json
"mcpServers": {
    "doc-finder": {
      "command": "uvx",
      "args": ["git+https://github.com/jerilseb/doc-finder-mcp"],
      "env": {
        "DOCS_REPO": "jerilseb/my-docs"
      }
    },
}
```

### GitHub Repository (Private)

If the documentation is stored in a private GitHub repository:


```json
"mcpServers": {
    "doc-finder": {
      "command": "uvx",
      "args": ["git+https://github.com/jerilseb/doc-finder-mcp"],
      "env": {
        "DOCS_REPO": "jerilseb/my-docs",
        "GITHUB_PAT": "<github_pat>"
      }
    },
}
```

### Local Filesystem

If you want to read documentation from a local directory instead of GitHub:

```json
"mcpServers": {
    "doc-finder": {
      "command": "uvx",
      "args": ["git+https://github.com/jerilseb/doc-finder-mcp"],
      "env": {
        "DOCS_FOLDER": "/path/to/your/docs"
      }
    },
}
```

## Directory Structure

Whether using GitHub or local filesystem, the documentation should be organized with 2 top level directories - `documentation` and `guidelines`. For example:

```
├── documentation
│   ├── gemini_live_api.md
│   ├── openai_agents_sdk.md
│   ├── openai_realtime_api.md
│   ├── supabase.md
│   └── tailwind_css.md
└── guidelines
    ├── chrome_extension.md
    ├── fastapi.md
    ├── sign_in_with_google.md
    └── vue_js.md
```

## License

MIT