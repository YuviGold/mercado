import logging
import re
from dataclasses import dataclass
from functools import cache
from http import HTTPStatus
from os import environ
from typing import Callable

from requests import Session

from ..utils import (choose_url, create_session, get_architecture_variations,
                     is_valid_architecture)
from .url_fetcher import URLDownloader
from .vendor import Installer, Tool, ToolVendor


@dataclass(frozen=True)
class GitHubTool(Tool):
    repository: str = ''
    asset_template: Callable[[str, str], str] = None


class GitHub(ToolVendor):
    def __init__(self):
        self._token = self._get_local_token()

    def _get_local_token(self):
        # TODO: Make more sophisticated
        return environ.get('GITHUB_TOKEN')

    def _session(self) -> Session:
        s = create_session()
        if self._token:
            s.headers = {'Authorization': 'Bearer ' + self._token}
        return s

    def _get_latest_release(self, tool: GitHubTool):
        res = self._session().get(f'https://api.github.com/repos/{tool.repository}/releases/latest')
        if res.status_code == HTTPStatus.NOT_FOUND.value:
            raise ValueError(f'tool {tool.repository} was not found')
        res.raise_for_status()
        return res.json()

    def _get_release_by_tag(self, tool: GitHubTool, tag: str):
        res = self._session().get(
            f'https://api.github.com/repos/{tool.repository}/releases/tags/{tag}')
        if res.status_code == HTTPStatus.NOT_FOUND.value:
            raise ValueError(f'version {tag} was not found for {tool.repository}')

        res.raise_for_status()
        return res.json()

    def _get_asset_url(self, tool: GitHubTool, os: str, arch: str, assets: list[dict[str]]) -> str:
        valid_assets_urls = []

        logging.debug(f"Found the following assets: {list(map(lambda asset: asset['name'], assets))}")

        templates = []
        if tool.asset_template:
            for arch in get_architecture_variations(arch):
                templates.append(tool.asset_template(os, arch))
            logging.debug(f"Tool {tool.name} has the following asset templates: {templates}")

        for asset in assets:
            for template in templates:
                if re.search(asset['name'], template, re.IGNORECASE):
                    return asset['browser_download_url']

            if re.search(tool.name, asset['name'], re.IGNORECASE) and \
               re.search(os, asset['name'], re.IGNORECASE) and \
               is_valid_architecture(expected=arch, actual=asset['name']):
                valid_assets_urls.append(asset['browser_download_url'])

        logging.debug(f"Looking for the best url from: {valid_assets_urls}")
        return choose_url(valid_assets_urls)

    @cache
    def get_latest_version(self, tool: GitHubTool):
        return self._get_latest_release(tool)['tag_name']

    @cache
    def get_installer(self, tool: GitHubTool, version: str, os: str, arch: str) -> Installer:
        res = self._get_release_by_tag(tool, version)
        url = self._get_asset_url(tool, os, arch, res['assets'])
        if not url:
            raise ValueError(f'There is no available asset {tool.name} for {os=}, {arch=}, {version=}')

        return URLDownloader(tool.name, version, url)
