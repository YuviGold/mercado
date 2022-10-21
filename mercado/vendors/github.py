import logging
import re
from dataclasses import dataclass
from http import HTTPStatus
from os import environ

from requests import Session

from ..utils import choose_url, create_session, is_valid_architecture
from .vendor import Artifact, Tool, ToolVendor


@dataclass
class GitHubTool(Tool):
    name: str
    repository: str = ''
    # render_function: Callable[[str, str, str], str]


class GitHub(ToolVendor):
    def __init__(self):
        self._token = self._get_local_token()

    @staticmethod
    def get_name() -> str:
        return 'github'

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

    def _get_asset_url(self, name: str, os: str, arch: str, assets: list[dict[str]]) -> str:
        valid_assets_urls = []

        logging.debug(f"Found the following assets: {list(map(lambda asset: asset['name'], assets))}")

        for asset in assets:
            # TODO: Currently it only validates os and arch within the name,
            # in case it would require manipulation - the render_function will return
            if re.search(name, asset['name'], re.IGNORECASE) and \
               re.search(os, asset['name'], re.IGNORECASE) and \
               is_valid_architecture(expected=arch, actual=asset['name']):
                valid_assets_urls.append(asset['browser_download_url'])

        logging.debug(f"Looking for the best url from: {valid_assets_urls}")
        return choose_url(valid_assets_urls)

    def get_release_by_version(self, tool: GitHubTool, version: str, os: str, arch: str) -> Artifact:
        res = self._get_release_by_tag(tool, version)
        url = self._get_asset_url(tool.name, os, arch, res['assets'])
        if not url:
            raise ValueError(f'There is no available artifact {tool.name} for {os=}, {arch=}, {version=}')

        return Artifact(tool.name, os, arch, res['tag_name'], url)

    def get_latest_release(self, tool: GitHubTool, os: str, arch: str) -> Artifact:
        res = self._get_latest_release(tool)
        version = res['tag_name']
        url = self._get_asset_url(tool.name, os, arch, res['assets'])
        if not url:
            raise ValueError(
                f'There is no available artifact {tool.name} for {os=}, {arch=} for latest version {version=}')

        return Artifact(tool.name, os, arch, res['tag_name'], url)
