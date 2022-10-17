import requests

from ..utils import is_valid_architecture
from .vendor import Product, ToolVendor


class HashiCorpTools(ToolVendor):
    def __init__(self):
        # TODO: Need to run e2e tests that all products actually available
        # self._products = self._get_hashicorp_products()
        self._products = ['vagrant', 'vault', 'terraform']

    def _get_hashicorp_products(self):
        res = requests.get('https://api.releases.hashicorp.com/v1/products')
        res.raise_for_status()
        return res.json()

    def _get_hashicorp_product_releases(self, product: str, version: str = ''):
        if product not in self._products:
            raise ValueError(product)

        if version:
            res = requests.get(
                f'https://api.releases.hashicorp.com/v1/releases/{product}/{version}?license_class=oss')
        else:
            res = requests.get(
                f'https://api.releases.hashicorp.com/v1/releases/{product}?license_class=oss')
        res.raise_for_status()
        return res.json()

    def _get_hashicorp_latest_release(self, product: str):
        # Results are ordered by release creation time from newest to oldest
        data = self._get_hashicorp_product_releases(product)
        return data[0]

    def _get_build_url(self, os: str, arch: str, builds: list[dict[str, str]]) -> str:
        for item in builds:
            if os == item['os'] and is_valid_architecture(expected=arch, actual=item['arch']):
                return item['url']

    def get_supported_products(self) -> list[str]:
        return self._products

    def get_release_by_version(self, name: str, version: str, os: str, arch: str) -> Product:
        res = self._get_hashicorp_product_releases(name, version)
        url = self._get_build_url(os, arch, res['builds'])
        if not url:
            raise ValueError(
                f'There is no available artifact {name} for {os=}, {arch=}, {version=}')

        return Product(name, os, arch, version, url)

    def get_latest_release(self, name: str, os: str, arch: str) -> Product:
        res = self._get_hashicorp_latest_release(name)
        version = res['version']
        url = self._get_build_url(os, arch, res['builds'])
        if not url:
            raise ValueError(
                f'There is no available artifact {name} for {os=}, {arch=} for latest version {version=}')

        return Product(name, os, arch, version, url)
