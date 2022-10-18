import pytest
from mercado.vendors.hashicorp import Hashicorp
from mercado.vendors.vendor import ToolVendor


def test_get_hashicorp_products(hashicorp: ToolVendor):
    assert all(elem in hashicorp._get_hashicorp_products()
               for elem in hashicorp.get_supported_products())


@pytest.mark.parametrize("product", Hashicorp().get_supported_products())
def test_get_release_by_version(hashicorp: ToolVendor, product: str, os: str, arch: str):
    for product in hashicorp.get_supported_products():
        release = hashicorp.get_latest_release(product, os, arch)
        assert release
        assert hashicorp.get_release_by_version(
            product, release.version, os, arch) == release


def test_get_latest_release_invalid_product(hashicorp: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        hashicorp.get_latest_release("invalid", os, arch)


def test_get_release_invalid_version(hashicorp: ToolVendor, os: str, arch: str):
    with pytest.raises(ValueError):
        hashicorp.get_release_by_version(
            hashicorp.get_supported_products()[0], "invalid", os, arch)
