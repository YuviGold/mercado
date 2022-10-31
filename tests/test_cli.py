import pytest
from mercado.cli import install_tool, is_latest
from mercado.tool_manager import ToolManager


@pytest.mark.parametrize("vendor,tool",
                         [(vendor, tools[0].name) for vendor, tools in ToolManager().get_supported_tools()])
def test_download_invalid_version(vendor: str, tool: str, os: str, arch: str):
    with pytest.raises(BaseException):
        install_tool(names=[f"{tool}@invalid"], os=os, arch=arch, dry_run=False)


@pytest.mark.parametrize("tool", [t.name for _, tools in ToolManager().get_supported_tools() for t in tools])
def test_download_and_verify_latest(tool: str, os: str, arch: str):
    install_tool(names=[tool], os=os, arch=arch, dry_run=False)
    is_latest(tool)
