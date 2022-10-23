import logging

from .tools import TOOLS
from .vendors.vendor import Artifact, Tool, ToolVendor


class ToolManager:
    def __init__(self) -> None:
        self._vendors: dict[ToolVendor, list[Tool]] = TOOLS

    def _get_tool(self, name) -> tuple[ToolVendor, Tool]:
        for vendor, tools in self._vendors.items():
            for tool in tools:
                if tool.name == name:
                    return vendor, tool
        raise ValueError(f"Tool '{name}' is not supported. Check the full supported tools with 'marcado list'")

    def get_supported_tools(self) -> list[tuple[str, list[Tool]]]:
        for vendor, tools in self._vendors.items():
            yield vendor.__class__.__name__, sorted(tools, key=lambda tool: tool.name)

    def get_release(self, name: str, os: str, arch: str) -> Artifact:
        version = None
        if '@' in name:
            version = name.split('@')[1]
            name = name[:name.index('@')]

        vendor, tool = self._get_tool(name)
        logging.info(f"'{name}' is available by the '{vendor.__class__.__name__}' vendor")

        if version:
            logging.info(f"Looking for '{tool.name}' with version {version} for {os} and {arch}")
            return vendor.get_release_by_version(tool, version, os, arch)
        else:
            logging.info(f"Looking for the latest version of '{tool.name}' for {os} and {arch}")
            return vendor.get_latest_release(tool, os, arch)
