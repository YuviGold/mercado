import pytest
from mercado.tool_manager import ToolManager


def test_get_release_invalid_product(toolmanager: ToolManager, os: str, arch: str):
    with pytest.raises(ValueError):
        toolmanager.get_release("invalid", os, arch)


def test_get_latest_release(toolmanager: ToolManager, os: str, arch: str):
    for _, products in toolmanager.get_supported_products():
        for product in products:
            assert toolmanager.get_release(product, os, arch)


def test_get_release_invalid_version(toolmanager: ToolManager, os, arch):
    with pytest.raises(ValueError):
        toolmanager.get_release(f"{toolmanager._vendors[0].get_supported_products()[0]}@invalid", os, arch)
