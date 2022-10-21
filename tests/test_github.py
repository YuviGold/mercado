import pytest
from mercado.vendors.github import GitHubTool
from mercado.vendors.vendor import ToolVendor


def test_get_latest_release_invalid_tool(github: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        github.get_latest_release(GitHubTool("invalid", repository="invalid"), os, arch)
