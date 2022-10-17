import itertools

from mercado.vendors.github import GitHubTools

from .vendors.hashicorp import HashiCorpTools
from .vendors.vendor import Product, ToolVendor


class ToolManager:
    def __init__(self) -> None:
        self._tool_owners: list[ToolVendor] = [HashiCorpTools(), GitHubTools()]

    def _get_tool_owner_by_product(self, name) -> ToolVendor:
        for tool_owner in self._tool_owners:
            if name in tool_owner.get_supported_products():
                return tool_owner
        raise ValueError(
            f'Tool {name} is not yet supported. Check the full supported tools with "marcado list"')

    def get_supported_products(self) -> list[str]:
        return list(itertools.chain.from_iterable(map(lambda x: x.get_supported_products(), self._tool_owners)))

    def get_release(self, name: str, os: str, arch: str) -> Product:
        version = None
        if '@' in name:
            version = name.split('@')[1]
            name = name[:name.index('@')]

        tool_owner = self._get_tool_owner_by_product(name)

        if version:
            return tool_owner.get_release_by_version(name, version, os, arch)
        else:
            return tool_owner.get_latest_release(name, os, arch)
