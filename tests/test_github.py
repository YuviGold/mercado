import pytest
from mercado.vendors.github import GitHub, GitHubTool


def test_get_latest_release_invalid_tool(github: GitHub):
    with pytest.raises(ValueError):
        github._get_latest_release(GitHubTool("invalid", repository="invalid"))
