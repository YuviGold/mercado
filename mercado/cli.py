import logging
from os import environ
from sys import exit

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from typer import Exit, Option, Typer

from .tool_manager import manager
from .utils import get_host_architecture, get_host_operating_system
from .vendors.vendor import Label

app = Typer()
console = Console()


def pretty_status(exists, is_latest):
    if exists and not is_latest:
        return ':arrow_double_up:'
    return pretty_bool(exists)


def pretty_bool(condition: bool) -> str:
    return ':white_check_mark:' if condition else ':cross_mark:'


@app.command('list', help='List all available tools')
def list_tools(filter_labels: list[Label] = Option(None, "--label", "-l"),
               verbose: bool = Option(False),
               names_only: bool = Option(False),
               with_labels: bool = Option(False),
               all: bool = Option(False)):
    table = Table(title="Mercado tools", header_style="bold magenta")
    table.add_column("Name", style="bold")

    if not names_only:
        if verbose:
            table.add_column("Vendor")

        if with_labels:
            table.add_column("Labels")
        table.add_column("Installed")

    for vendor, tools in manager.get_supported_tools(separate_vendors=verbose):
        if verbose:
            table.add_section()

        for tool in tools:
            if filter_labels:
                if not any([label in tool.labels for label in filter_labels]):
                    continue

            exists, is_latest, version, path, _ = manager.get_status(tool.name)
            if not exists and not all:
                continue

            if names_only:
                table.add_row(tool.name)
                continue

            exists_string = pretty_status(exists, is_latest)

            if verbose:
                if exists:
                    exists_string += f' ({path} {version})'

                if with_labels:
                    table.add_row(tool.name, vendor, ','.join(map(lambda item: item.value, tool.labels)), exists_string)
                else:
                    table.add_row(tool.name, vendor, exists_string)
            else:
                if with_labels:
                    table.add_row(tool.name, ','.join(map(lambda item: item.value, tool.labels)), exists_string)
                else:
                    table.add_row(tool.name, exists_string)

    console.print(table)


@app.command('install', help='Install a tool')
def install_tool(names: list[str],
                 os: str = Option(get_host_operating_system()),
                 arch: str = Option(get_host_architecture()),
                 dry_run: bool = Option(False, envvar='DRY_RUN')):
    for name in names:
        installer = manager.get_installer(name, os, arch)
        logging.debug(f"'{installer.name}' was found with version '{installer.version}'")

        if not dry_run:
            logging.info(f"Installing '{installer.name}'...")
            installer.install()
            console.print(f":thumbs_up:\t'{name}' version {installer.version} is installed")


@app.command('is-latest', help='Check if the current version is the latest one')
def get_status(name: str):
    logging.disable(level=logging.WARNING)

    _, is_latest, local_version, _, latest_version = manager.get_status(name)

    if not is_latest:
        console.print(f":thumbs_down:\t'{name}' version '{latest_version}' is available! (current: {local_version})")
        raise Exit(code=1)
    else:
        console.print(f":thumbs_up:\tYou have the latest version of '{name}' ({local_version})")


@app.command('show', help='Print information about the supported tool')
def show(name: str):
    logging.disable(level=logging.WARNING)

    exists, is_latest, local_version, path, latest_version = manager.get_status(name)

    console.print(f'Name: {name}')
    console.print(f'Status: {pretty_status(exists, is_latest)}')

    if exists:
        console.print(f'Local Version: {local_version}')
        console.print(f'Path: {path}')
    console.print(f'Remote Version: {latest_version}')


def init_logger():
    LOGLEVEL = environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL,
                        format='%(message)s',
                        handlers=[RichHandler(show_level=False, show_path=False)])


def main():
    init_logger()

    try:
        app()
    except ValueError as ex:
        console.print(f':no_entry_sign:\t{ex}')
        exit(1)
