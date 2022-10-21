from http import HTTPStatus

from ..utils import choose_url, create_session, is_valid_architecture
from .vendor import Artifact, Tool, ToolVendor


class Hashicorp(ToolVendor):
    def __init__(self):
        self._products = self._get_hashicorp_products()

    @staticmethod
    def get_name() -> str:
        return 'hashicorp'

    def _get_hashicorp_products(self):
        res = create_session().get('https://api.releases.hashicorp.com/v1/products')
        res.raise_for_status()
        return res.json()

    def _get_hashicorp_product_releases(self, name: str, version: str = ''):
        if name not in self._products:
            raise ValueError(name)

        if version:
            res = create_session().get(
                f'https://api.releases.hashicorp.com/v1/releases/{name}/{version}?license_class=oss')
            if res.status_code == HTTPStatus.NOT_FOUND.value:
                raise ValueError(f'version {version} was not found for {name}')
        else:
            res = create_session().get(f'https://api.releases.hashicorp.com/v1/releases/{name}?license_class=oss')
        res.raise_for_status()
        return res.json()

    def _get_hashicorp_latest_release(self, name: str):
        # Results are ordered by release creation time from newest to oldest
        data = self._get_hashicorp_product_releases(name)
        return data[0]

    def _get_build_url(self, os: str, arch: str, builds: list[dict[str, str]]) -> str:
        valid_assets_urls = []

        for item in builds:
            if os == item['os'] and is_valid_architecture(expected=arch, actual=item['arch']):
                valid_assets_urls.append(item['url'])

        return choose_url(valid_assets_urls)

    def get_release_by_version(self, tool: Tool, version: str, os: str, arch: str) -> Artifact:
        res = self._get_hashicorp_product_releases(tool.name, version)
        url = self._get_build_url(os, arch, res['builds'])
        if not url:
            raise ValueError(f'There is no available artifact {tool.name} for {os=}, {arch=}, {version=}')

        return Artifact(tool.name, os, arch, version, url)

    def get_latest_release(self, tool: Tool, os: str, arch: str) -> Artifact:
        res = self._get_hashicorp_latest_release(tool.name)
        version = res['version']
        url = self._get_build_url(os, arch, res['builds'])
        if not url:
            raise ValueError(
                f'There is no available artifact {tool.name} for {os=}, {arch=} for latest version {version=}')

        return Artifact(tool.name, os, arch, version, url)
