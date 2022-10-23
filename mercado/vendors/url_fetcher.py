
import logging
from dataclasses import dataclass
from functools import partial
from http import HTTPStatus
from typing import Callable

from ..utils import create_session, fetch_url, get_architecture_variations
from .vendor import Artifact, Tool, ToolVendor


@dataclass
class URLFetcherTool(Tool):
    get_latest_version_url: str = ''
    get_latest_release_url: Callable[[str, str], str] = None
    get_release_by_version_url: Callable[[str, str, str], str] = None


class URLFetcher(ToolVendor):
    def _check_urls(self, tool: URLFetcherTool, os: str, arch: str,
                    url_template: Callable[[str, str], str]) -> str:
        urls = []
        for arch in get_architecture_variations(arch):
            urls.append(url_template(os, arch))

        logging.debug(f"Tool {tool.name} has the following urls: {urls}")

        for url in urls:
            res = create_session().head(url)
            if res.status_code == HTTPStatus.NOT_FOUND.value:
                logging.debug(f'URL {url} was not found')
                continue
            if res.status_code == HTTPStatus.OK.value:
                return url

        raise ValueError(f'{tool.name} URL is not valid')

    def get_latest_release(self, tool: URLFetcherTool, os: str, arch: str) -> Artifact:
        assert tool.get_latest_release_url or tool.get_latest_version_url

        if tool.get_latest_version_url:
            version = fetch_url(tool.get_latest_version_url)
            return self.get_release_by_version(tool, version, os, arch)

        if tool.get_latest_release_url:
            url = self._check_urls(tool, os, arch, tool.get_latest_release_url)
            return Artifact(tool.name, os, arch, version, url)

        raise NotImplementedError()

    def get_release_by_version(self, tool: URLFetcherTool, version: str, os: str, arch: str) -> Artifact:
        url = self._check_urls(tool, os, arch, partial(tool.get_release_by_version_url, version=version))
        return Artifact(tool.name, os, arch, version, url)
