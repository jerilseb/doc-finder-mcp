# Doc Finder MCP Server

A Model Context Protocol server that allows you fetch documentation or coding guidelines stored in a github repository, on demand.


## Installation

Install [uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### In your MCP client configuration:

The `uvx` command is provided by uv and allows you to run Python packages directly:

If the documentation is stored in a public repo,

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

If the documentation is stored in a private repo,


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

The DOCS_REPO should contain 2 top level directores - `documentation` and `guidelines`. For example

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