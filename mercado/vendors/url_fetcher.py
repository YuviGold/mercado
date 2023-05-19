
import logging
from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from typing import Callable

from ..utils import (create_session, default_install_path, download_url,
                     fetch_url, get_architecture_variations,
                     get_operating_system_variations)
from .vendor import Installer, Tool, ToolVendor


@dataclass(frozen=True)
class URLFetcherTool(Tool):
    get_latest_version_url: str = ''
    get_release_by_version_url: Callable[[str, str, str], str] = None


class URLFetcher(ToolVendor):
    def _check_urls(self, tool: URLFetcherTool, os: str, arch: str, version: str,
                    url_template: Callable[[str, str], str]) -> str:
        urls = []
        for arch in get_architecture_variations(arch):
            for os in get_operating_system_variations(os):
                urls.append(url_template(os, arch, version))

        logging.debug(f"Tool {tool.name} has the following urls: {urls}")

        for url in urls:
            res = create_session().head(url)
            if res.status_code == HTTPStatus.NOT_FOUND.value:
                logging.debug(f'URL {url} was not found')
                continue
            if res.status_code == HTTPStatus.OK.value:
                return url

        raise ValueError(f'{tool.name} URL is not valid')

    def get_latest_version(self, tool: URLFetcherTool) -> str:
        return fetch_url(tool.get_latest_version_url)

    def get_installer(self, tool: URLFetcherTool, version: str, os: str, arch: str) -> Installer:
        url = self._check_urls(tool, os, arch, version, tool.get_release_by_version_url)
        return URLDownloader(tool.name, version, url, tool.target)


class URLDownloader(Installer):
    def __init__(self, name: str, version: str, url: str, target: Path):
        self.name = name
        self.version = version
        self._url = url
        self.target = target if target else default_install_path(self.name)

    def install(self):
        download_url(self.name, self._url, self.target)
