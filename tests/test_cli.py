import pytest

from mercado.cli import get_status, install_tool, uninstall_tool
from mercado.tool_manager import ToolManager


@pytest.mark.parametrize(
    "vendor,tool", [(vendor, tools[0].name) for vendor, tools in ToolManager().get_supported_tools()]
)
def test_download_invalid_version(vendor: str, tool: str, os: str, arch: str):
    with pytest.raises(BaseException):
        install_tool(names=[f"{tool}@invalid"], os=os, arch=arch, dry_run=False)


@pytest.mark.parametrize("tool", [t.name for _, tools in ToolManager().get_supported_tools() for t in tools])
def test_download_verify_latest_uninstall(tool: str, os: str, arch: str):
    install_tool(names=[tool], os=os, arch=arch, dry_run=False)
    get_status(tool)

    if tool in ("docker", ):
        # TODO: Convert uninstall script to be per tool
        pytest.xfail("Docker cannot be uninstalled at the moment.")

    uninstall_tool(names=[tool], dry_run=False)
