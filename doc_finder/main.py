import os
import base64
import asyncio
from pathlib import Path
from typing import List, Optional

import httpx
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base

# Initialize the MCP server
mcp = FastMCP("DocFinder")

# Configuration
GITHUB_PAT = os.environ.get("GITHUB_PAT")
DOCS_REPO = os.environ.get("DOCS_REPO")
DOCS_FOLDER = os.environ.get("DOCS_FOLDER")

# Validate that at least one source is configured
if not DOCS_REPO and not DOCS_FOLDER:
    raise ValueError("Either DOCS_REPO or DOCS_FOLDER environment variable is required")

# Validate DOCS_FOLDER exists if provided
if DOCS_FOLDER and not Path(DOCS_FOLDER).is_dir():
    raise ValueError(f"DOCS_FOLDER path does not exist or is not a directory: {DOCS_FOLDER}")

USE_LOCAL_DOCS = bool(DOCS_FOLDER)

GITHUB_API_BASE = "https://api.github.com"


def _get_github_headers() -> dict:
    """Get headers for GitHub API requests."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DocFinder-MCP",
    }
    if GITHUB_PAT:
        headers["Authorization"] = f"token {GITHUB_PAT}"
    return headers


async def _get_all_markdown_files_local(directory: str) -> List[str]:
    """Get all markdown files from local directory."""
    try:
        base_path = Path(DOCS_FOLDER)
        dir_path = base_path / directory
        
        if not dir_path.exists() or not dir_path.is_dir():
            return []
        
        markdown_files = []
        for file_path in dir_path.glob("*.md"):
            relative_path = f"{directory}/{file_path.name}"
            markdown_files.append(relative_path)
        
        return markdown_files
    except Exception:
        return []


async def _get_all_markdown_files_github(directory: str) -> List[str]:
    """Get all markdown files from GitHub repository directory."""
    try:
        headers = _get_github_headers()
        url = f"{GITHUB_API_BASE}/repos/{DOCS_REPO}/contents/{directory}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            contents = response.json()
            markdown_files = []

            for item in contents:
                if item["type"] == "file" and item["name"].endswith(".md"):
                    markdown_files.append(f"{directory}/{item['name']}")

        return markdown_files
    except Exception:
        return []


async def _get_all_markdown_files(directory: str) -> List[str]:
    """Get all markdown files from configured source (local or GitHub)."""
    if USE_LOCAL_DOCS:
        return await _get_all_markdown_files_local(directory)
    else:
        return await _get_all_markdown_files_github(directory)


async def _get_file_content_from_local(filepath: str) -> Optional[str]:
    """Get the content of a specific file from local filesystem."""
    try:
        base_path = Path(DOCS_FOLDER)
        file_path = base_path / filepath
        
        if not file_path.exists() or not file_path.is_file():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


async def _get_file_content_from_github(
    client: httpx.AsyncClient, filepath: str
) -> Optional[str]:
    """Get the content of a specific file from GitHub repository."""
    try:
        headers = _get_github_headers()
        url = f"{GITHUB_API_BASE}/repos/{DOCS_REPO}/contents/{filepath}"

        response = await client.get(url, headers=headers)
        response.raise_for_status()

        file_data = response.json()
        if file_data["type"] == "file":
            # Decode base64 content
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            return content
        return None
    except Exception:
        return None


async def _get_file_content(filepath: str) -> Optional[str]:
    """Get the content of a specific file from configured source (local or GitHub)."""
    if USE_LOCAL_DOCS:
        return await _get_file_content_from_local(filepath)
    else:
        async with httpx.AsyncClient() as client:
            return await _get_file_content_from_github(client, filepath)


@mcp.tool()
async def get_file_contents(filenames: List[str]) -> str:
    """
    Get the full content of specific files.

    Args:
        filenames: A list of relative paths to the files (eg: ["documentation/library.md", "guidelines/style.md"])

    Returns:
        The full content of the requested files, concatenated together.
    """
    contents = []

    # Fetch all files in parallel
    tasks = [_get_file_content(filename) for filename in filenames]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for filename, content in zip(filenames, results):
        if isinstance(content, str) and content:
            contents.append(f"# File: {filename}\n\n{content}\n\n---")

    return "\n\n".join(contents)


@mcp.tool()
async def list_all_development_guidelines() -> str:
    """
    List all available development or coding guidelines files.

    Returns:
        A list of all development or coding guidelines files
    """
    markdown_files = await _get_all_markdown_files("guidelines")
    if not markdown_files:
        return "No development guidelines files found in the specified directory."

    output = "All Development guidelines:\n\n"

    for file_path in sorted(markdown_files):
        output += f"- {file_path}\n"

    return output


@mcp.tool()
async def list_all_documentation() -> str:
    """
    List all available documentation files.

    Returns:
        A list of all documentation files
    """
    markdown_files = await _get_all_markdown_files("documentation")
    if not markdown_files:
        return "No documentation files found in the specified directory."

    output = "All Docs:\n\n"

    for file_path in sorted(markdown_files):
        output += f"- {file_path}\n"

    return output


@mcp.prompt()
def read_guidelines(topic: str) -> str:
    return f"Read the development guidelines about {topic}"


@mcp.prompt()
def read_documentation(topic: str) -> str:
    return f"Read the documentation about {topic}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
