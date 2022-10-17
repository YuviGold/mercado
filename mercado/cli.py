import logging
import platform
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from typer import Option, Typer

from .tool_manager import ToolManager
from .utils import download, get_local_version

app = Typer()
console = Console()


def pretty_bool(condition: bool) -> str:
    return ':white_check_mark:' if condition else ':cross_mark:'


@app.command('list', help='List all available tools')
def list_tools(verbose: bool = Option(False)):
    manager = ToolManager()

    table = Table(title="Mercado tools")
    table.add_column("Name")
    table.add_column("Vendor")
    table.add_column("Exists")

    for vendor, products in manager.get_supported_products():
        table.add_section()
        for product in products:
            exists = True
            try:
                version, path = get_local_version(product)
            except ValueError:
                exists = False

            local_string = pretty_bool(exists)
            if exists and verbose:
                local_string += f' ({path} {version})'
            table.add_row(product, vendor, local_string)

    console.print(table)


@app.command('install', help='Install a tool')
def install_product(names: list[str],
                    os: Optional[str] = Option(platform.system().lower()),
                    arch: Optional[str] = Option(platform.machine()),
                    dry_run: bool = Option(False, envvar='DRY_RUN')):
    manager = ToolManager()

    for name in names:
        release = manager.get_release(name, os, arch)

        if not dry_run:
            download(name, release.url)


@app.command('is-latest', help='Check if the current version is the latest one')
def is_latest(name: str):
    local_version, path = get_local_version(name)
    logging.info(f"'{name}' was found at {path} with version {local_version}")

    manager = ToolManager()
    latest_version = manager.get_release(
        name, platform.system().lower(), platform.machine()).version
    if local_version not in latest_version:
        console.print(
            f"'{name}' version {latest_version} is available! (current: {local_version})")
    else:
        console.print(
            f":thumbs_up: You have the latest version of '{name}' ({local_version})")


def init_logger():
    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        handlers=[RichHandler()])


def main():
    init_logger()

    try:
        app()
    except ValueError as ex:
        console.print(f':no_entry_sign: {ex}')
