import pytest
from mercado.tool_manager import ToolManager


def test_get_release_invalid_tool(toolmanager: ToolManager, os: str, arch: str):
    with pytest.raises(ValueError):
        toolmanager.get_release("invalid", os, arch)


@pytest.mark.parametrize("tool", [t.name for _, tools in ToolManager().get_supported_tools() for t in tools])
def test_get_latest_release(toolmanager: ToolManager, tool, os: str, arch: str):
    release = toolmanager.get_release(tool, os, arch)
    assert toolmanager.get_release(f"{tool}@{release.version}", os, arch) == release


@pytest.mark.parametrize("vendor,tool", [(vendor, tools[0].name) for vendor, tools in ToolManager().get_supported_tools()])
def test_get_release_invalid_version(toolmanager: ToolManager, vendor: str, tool: str, os: str, arch: str):
    with pytest.raises(ValueError):
        toolmanager.get_release(f"{tool}@invalid", os, arch)
