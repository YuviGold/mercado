import logging
from os import environ
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from typer import Option, Typer

from .tool_manager import ToolManager
from .utils import (get_host_architecture, get_host_operating_system,
                    get_local_version, is_tool_available_in_path)
from .vendors.vendor import Label

app = Typer()
console = Console()
manager = ToolManager()


def pretty_bool(condition: bool) -> str:
    return ':white_check_mark:' if condition else ':cross_mark:'


@app.command('list', help='List all available tools')
def list_tools(filter_labels: list[Label] = Option(None, "--label", "-l"),
               verbose: bool = Option(False),
               installed_only: bool = Option(False)):
    table = Table(title="Mercado tools")
    table.add_column("Name")

    if verbose:
        table.add_column("Vendor")

    table.add_column("Labels")
    table.add_column("Exists")

    for vendor, tools in manager.get_supported_tools():
        table.add_section()
        for tool in tools:
            if filter_labels:
                if not any([label in tool.labels for label in filter_labels]):
                    continue

            exists = is_tool_available_in_path(tool.name)
            if installed_only and not exists:
                continue

            exists_string = pretty_bool(exists)

            if verbose:
                if exists:
                    version, path = get_local_version(tool.name)
                    exists_string += f' ({path} {version})'
                table.add_row(tool.name, vendor, ','.join(map(lambda item: item.value, tool.labels)), exists_string)
            else:
                table.add_row(tool.name, ','.join(map(lambda item: item.value, tool.labels)), exists_string)

    console.print(table)


@app.command('install', help='Install a tool')
def install_tool(names: list[str],
                 os: Optional[str] = Option(get_host_operating_system()),
                 arch: Optional[str] = Option(get_host_architecture()),
                 dry_run: bool = Option(False, envvar='DRY_RUN')):
    for name in names:
        installer = manager.get_installer(name, os, arch)
        logging.debug(f"'{installer.name}' was found with version '{installer.version}'")

        if not dry_run:
            logging.info(f"Installing '{installer.name}'...")
            installer.install()
            console.print(f":thumbs_up:\t'{name}' version {installer.version} is installed")


@app.command('is-latest', help='Check if the current version is the latest one')
def is_latest(name: str):
    logging.disable(level=logging.WARNING)

    local_version, path = get_local_version(name)
    logging.info(f"'{name}' was found at {path} with version {local_version}")

    latest_version = manager.get_latest_version(name)
    if local_version not in latest_version:
        console.print(f":thumbs_down:\t'{name}' version '{latest_version}' is available! (current: {local_version})")
    else:
        console.print(f":thumbs_up:\tYou have the latest version of '{name}' ({local_version})")


@app.command('show', help='Print information about the supported tool')
def show(name: str):
    logging.disable(level=logging.WARNING)

    exists = is_tool_available_in_path(name)
    latest_version = manager.get_latest_version(name)

    console.print(f'Name: {name}')
    console.print(f'Installed: {pretty_bool(exists)}')

    if exists:
        local_version, path = get_local_version(name)
        console.print(f'Local Version: {local_version}')
        console.print(f'Path: {path}')
    console.print(f'Remote Version: {latest_version}')


def init_logger():
    LOGLEVEL = environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL,
                        format='%(message)s',
                        handlers=[RichHandler()])


def main():
    init_logger()

    try:
        app()
    except ValueError as ex:
        console.print(f':no_entry_sign:\t{ex}')
