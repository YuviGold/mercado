from mercado.cli import *
import pytest


@pytest.mark.parametrize("product",
                         [p for _, products in ToolManager().get_supported_products() for p in products])
def test_download_and_verify_latest(product: str, os: str, arch: str):
    install_product(names=[product], os=os, arch=arch, dry_run=False)
    is_latest(product)
