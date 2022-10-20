import pytest
from mercado.tool_manager import ToolManager


def test_get_release_invalid_product(toolmanager: ToolManager, os: str, arch: str):
    with pytest.raises(ValueError):
        toolmanager.get_release("invalid", os, arch)


@pytest.mark.parametrize("product", [p for _, products in ToolManager().get_supported_products() for p in products])
def test_get_latest_release(toolmanager: ToolManager, product, os: str, arch: str):
    release = toolmanager.get_release(product, os, arch)
    assert toolmanager.get_release(f"{product}@{release.version}", os, arch) == release


def test_get_release_invalid_version(toolmanager: ToolManager, os, arch):
    with pytest.raises(ValueError):
        toolmanager.get_release(f"{toolmanager._vendors[0].get_supported_products()[0]}@invalid", os, arch)
