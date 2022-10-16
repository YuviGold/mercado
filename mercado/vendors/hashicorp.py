import requests

from .vendor import Product, ToolVendor


class HashiCorpTools(ToolVendor):
    def __init__(self):
        self._products = self._get_hashicorp_products()

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

    def get_supported_products(self) -> list[str]:
        return self._products

    def get_release_by_version(self, name: str, version: str) -> Product:
        res = self._get_hashicorp_product_releases(name, version)
        return Product(name, res['version'], res['builds'][0]['url'])

    def get_latest_release(self, name: str) -> Product:
        res = self._get_hashicorp_latest_release(name)
        return Product(name, res['version'], res['builds'][0]['url'])
