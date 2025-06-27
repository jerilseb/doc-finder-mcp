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
      "args": ["git+https://github.com/jerilseb/doc-finder-mcp"]
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
        "GITHUB_PAT": "<github_pat>"
      }
    },
}
```

## License

MIT