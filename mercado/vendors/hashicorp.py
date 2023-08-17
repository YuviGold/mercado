import logging
from functools import cache
from http import HTTPStatus

from ..utils import (choose_url, create_session, is_valid_architecture,
                     is_valid_os)
from .url_fetcher import URLDownloader
from .vendor import Installer, Tool, ToolVendor


class Hashicorp(ToolVendor):
    def __init__(self):
        self._products = self._get_hashicorp_products()

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

        logging.debug(f"Available builds: {[build['url'] for build in builds]}")

        for item in builds:
            if is_valid_os(expected=os, actual=item['os']) and \
               is_valid_architecture(expected=arch, actual=item['arch']):
                valid_assets_urls.append(item['url'])

        logging.debug(f"Looking for the best url from: {valid_assets_urls}")
        return choose_url(valid_assets_urls)

    @cache
    def get_latest_version(self, tool: Tool) -> str:
        return self._get_hashicorp_latest_release(tool.name)['version']

    @cache
    def get_installer(self, tool: Tool, version: str, os: str, arch: str) -> Installer:
        res = self._get_hashicorp_product_releases(tool.name, version)
        url = self._get_build_url(os, arch, res['builds'])
        if not url:
            raise ValueError(f'There is no available build {tool.name} for {os=}, {arch=}, {version=}')

        logging.debug(f'Found {tool.name} with version {version} on URL {url}')
        return URLDownloader(tool.name, version, url, tool.target)
