import pytest
from mercado.cli import install_tool, is_latest
from mercado.tool_manager import ToolManager


@pytest.mark.parametrize("tool", [t.name for _, tools in ToolManager().get_supported_tools() for t in tools])
def test_download_and_verify_latest(tool: str, os: str, arch: str):
    install_tool(names=[tool], os=os, arch=arch, dry_run=False)
    is_latest(tool)
