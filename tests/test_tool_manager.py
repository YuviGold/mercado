import pytest

from mercado.tool_manager import ToolManager


def test_get_installer_invalid_tool(toolmanager: ToolManager, os: str, arch: str):
    with pytest.raises(ValueError):
        toolmanager.get_installer("invalid", os, arch)


@pytest.mark.parametrize("tool", [t.name for _, tools in ToolManager().get_supported_tools() for t in tools])
def test_get_installer_happy_flow(toolmanager: ToolManager, tool: str, os: str, arch: str):
    installer = toolmanager.get_installer(tool, os, arch)
    assert toolmanager.get_installer(f"{tool}@{installer.version}", os, arch) == installer
