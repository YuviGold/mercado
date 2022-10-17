import logging

from .vendors.github import GitHub
from .vendors.hashicorp import Hashicorp
from .vendors.vendor import Product, ToolVendor


class ToolManager:
    def __init__(self) -> None:
        self._vendors: list[ToolVendor] = [Hashicorp(), GitHub()]

    def _get_vendor_by_product(self, name) -> ToolVendor:
        for vendor in self._vendors:
            if name in vendor.get_supported_products():
                return vendor
        raise ValueError(
            f"Tool '{name}' is not supported. Check the full supported tools with 'marcado list'")

    def get_supported_products(self) -> list[tuple[str, list[str]]]:
        for vendor in self._vendors:
            yield vendor.__class__.__name__, vendor.get_supported_products()

    def get_release(self, name: str, os: str, arch: str) -> Product:
        version = None
        if '@' in name:
            version = name.split('@')[1]
            name = name[:name.index('@')]

        vendor = self._get_vendor_by_product(name)
        logging.info(
            f"'{name}' is available by the '{vendor.__class__.__name__}' vendor")

        if version:
            logging.info(
                f"Looking for '{name}' with version {version} for {os} and {arch}")
            return vendor.get_release_by_version(name, version, os, arch)
        else:
            logging.info(
                f"Looking for the latest version of '{name}' for {os} and {arch}")
            return vendor.get_latest_release(name, os, arch)
