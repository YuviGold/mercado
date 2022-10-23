import logging

from .tools import TOOLS
from .utils import INSTALL_DIR
from .vendors.vendor import Installer, Tool, ToolVendor


class ToolManager:
    def __init__(self) -> None:
        self._vendors: dict[ToolVendor, list[Tool]] = TOOLS
        INSTALL_DIR.mkdir(exist_ok=True)

    def _get_tool(self, name) -> tuple[ToolVendor, Tool]:
        for vendor, tools in self._vendors.items():
            for tool in tools:
                if tool.name == name:
                    return vendor, tool
        raise ValueError(f"Tool '{name}' is not supported. Check the full supported tools with 'marcado list'")

    def get_supported_tools(self) -> list[tuple[str, list[Tool]]]:
        for vendor, tools in self._vendors.items():
            yield vendor.__class__.__name__, sorted(tools, key=lambda tool: tool.name)

    def get_latest_version(self, name: str) -> str:
        vendor, tool = self._get_tool(name)
        return vendor.get_latest_version(tool)

    def get_installer(self, name: str, os: str, arch: str) -> Installer:
        version = None
        if '@' in name:
            version = name.split('@')[1]
            name = name[:name.index('@')]

        vendor, tool = self._get_tool(name)
        logging.debug(f"'{name}' is available by the '{vendor.__class__.__name__}' vendor")

        if not version:
            logging.info(f"Looking for the latest version of '{tool.name}'")
            version = vendor.get_latest_version(tool)

        logging.info(f"Getting installer for tool '{tool.name}' with version {version} for {os} and {arch}")
        return vendor.get_installer(tool, version, os, arch)
