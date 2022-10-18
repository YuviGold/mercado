import pytest
from mercado.vendors.github import GitHub
from mercado.vendors.vendor import ToolVendor


@pytest.mark.parametrize("product", GitHub().get_supported_products())
def test_get_release_by_version(github: ToolVendor, product: str, os: str, arch: str):
    for product in github.get_supported_products():
        release = github.get_latest_release(product, os, arch)
        assert release
        assert github.get_release_by_version(
            product, release.version, os, arch) == release


def test_get_latest_release_invalid_product(github: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        github.get_latest_release("invalid", os, arch)


def test_get_release_invalid_version(github: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        github.get_release_by_version(
            github.get_supported_products()[0], "invalid", os, arch)
