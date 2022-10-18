from dataclasses import dataclass

import requests

from ..utils import choose_url, is_valid_architecture
from .vendor import Product, ToolVendor


@dataclass
class GitHubProduct:
    name: str
    repository: str
    # render_function: Callable[[str, str, str], str]


class GitHub(ToolVendor):
    def __init__(self):
        self.products: dict[str, GitHubProduct] = {
            'kind': GitHubProduct('kind', repository='kubernetes-sigs/kind'),
            'gh': GitHubProduct('gh', repository='cli/cli'),
        }

    def _get_latest_release(self, product: str):
        if product not in self.products:
            raise ValueError(product)

        res = requests.get(
            f'https://api.github.com/repos/{self.products[product].repository}/releases/latest')
        res.raise_for_status()
        return res.json()

    def _get_release_by_tag(self, product: str, tag: str):
        if product not in self.products:
            raise ValueError(product)

        res = requests.get(
            f'https://api.github.com/repos/{self.products[product].repository}/releases/tags/{tag}')
        if res.status_code == 404:
            raise ValueError(f'version {tag} was not found for {product}')

        res.raise_for_status()
        return res.json()

    def _get_asset_url(self, name: str, os: str, arch: str, assets: list[dict[str]]) -> str:
        valid_assets_urls = []

        for asset in assets:
            # TODO: Currently it only validates os and arch within the name,
            # in case it would require manipulation - the render_function will return
            if os in asset['name'] and is_valid_architecture(expected=arch, actual=asset['name']):
                valid_assets_urls.append(asset['browser_download_url'])

        return choose_url(valid_assets_urls)

    def get_supported_products(self) -> list[str]:
        return sorted(list(self.products.keys()))

    def get_release_by_version(self, name: str, version: str, os: str, arch: str) -> Product:
        res = self._get_release_by_tag(name, version)
        url = self._get_asset_url(name, os, arch, res['assets'])
        if not url:
            raise ValueError(
                f'There is no available artifact {name} for {os=}, {arch=}, {version=}')

        return Product(name, os, arch, res['tag_name'], url)

    def get_latest_release(self, name: str, os: str, arch: str) -> Product:
        res = self._get_latest_release(name)
        version = res['tag_name']
        url = self._get_asset_url(name, os, arch, res['assets'])
        if not url:
            raise ValueError(
                f'There is no available artifact {name} for {os=}, {arch=} for latest version {version=}')

        return Product(name, os, arch, res['tag_name'], url)
