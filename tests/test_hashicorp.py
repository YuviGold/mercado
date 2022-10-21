import pytest
from mercado.vendors.vendor import Tool, ToolVendor


def test_get_latest_release_invalid_tool(hashicorp: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        hashicorp.get_latest_release(Tool("invalid"), os, arch)
