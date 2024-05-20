import logging
from pathlib import Path

from .tools import TOOLS
from .utils import get_local_version, is_tool_available
from .vendors.vendor import Installer, Tool, ToolVendor


class ToolManager:
    def __init__(self) -> None:
        self._vendors: dict[ToolVendor, list[Tool]] = TOOLS

    def get_tool(self, name) -> Tool:
        _, tool = self._get_tool(name)
        return tool

    def _get_tool(self, name) -> tuple[ToolVendor, Tool]:
        for vendor, tools in self._vendors.items():
            for tool in tools:
                if tool.name == name:
                    return vendor, tool
        raise ValueError(f"Tool '{name}' is not supported. Check the full supported tools with 'marcado list'")

    def get_supported_tools(self, separate_vendors=False) -> list[tuple[str, list[Tool]]]:
        if not separate_vendors:
            all_vendors: list[tuple[str, Tool]] = []
            for vendor, tools in self._vendors.items():
                for tool in tools:
                    all_vendors.append((vendor.__class__.__name__, tool))
            for vendor_name, tool in sorted(all_vendors, key=lambda item: item[1].name):
                yield vendor_name, [tool]
        else:
            for vendor, tools in self._vendors.items():
                yield vendor.__class__.__name__, sorted(tools, key=lambda tool: tool.name)

    def get_latest_version(self, name: str) -> str:
        vendor, tool = self._get_tool(name)
        return vendor.get_latest_version(tool)

    def get_installer(self, name: str, os: str, arch: str) -> Installer:
        version = None
        if "@" in name:
            version = name.split("@")[1]
            name = name[: name.index("@")]

        vendor, tool = self._get_tool(name)
        logging.debug(f"'{name}' is available by the '{vendor.__class__.__name__}' vendor")

        if not version:
            logging.info(f"Looking for the latest version of '{tool.name}'")
            version = vendor.get_latest_version(tool)

        logging.info(f"Getting installer for tool '{tool.name}' with version {version} for {os} and {arch}")
        return vendor.get_installer(tool, version, os, arch)

    def is_tool_available(self, name: str) -> bool:
        return is_tool_available(self.get_tool(name))

    def get_status(self, name: str) -> tuple[bool, bool, str, Path | None, str]:
        exists = is_tool_available(self.get_tool(name))
        local_version = ""
        path = None
        latest_version = ""

        if exists:
            local_version, path = get_local_version(self.get_tool(name))
            latest_version = self.get_latest_version(name)

        # In is_latest release candidates are ignored
        is_latest = local_version.split('-rc')[0] in latest_version.split('-rc')[0]
        return exists, is_latest, local_version, path, latest_version


manager = ToolManager()
