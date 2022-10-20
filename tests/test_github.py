import pytest
from mercado.vendors.vendor import ToolVendor


def test_get_latest_release_invalid_product(github: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        github.get_latest_release("invalid", os, arch)


def test_get_release_invalid_version(github: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        github.get_release_by_version(github.get_supported_products()[0], "invalid", os, arch)
