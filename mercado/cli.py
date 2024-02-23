import logging
from os import environ
from sys import exit

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from typer import Context, Exit, Option, Typer

from .tool_manager import manager
from .utils import get_host_architecture, get_host_operating_system, get_local_version, is_tool_available, run_once
from .vendors.vendor import Label

app = Typer()
console = Console()


def pretty_status(exists, is_latest):
    if exists and not is_latest:
        return ":arrow_up_small:"
    return pretty_bool(exists)


def pretty_bool(condition: bool) -> str:
    return ":white_check_mark:" if condition else ":cross_mark:"


@app.command("list", help="List all available tools")
def list_tools(
    filter_labels: list[Label] = Option(None, "--label", "-l"),
    verbose: bool = Option(False, "--verbose", "-v"),
    names_only: bool = Option(False),
    with_labels: bool = Option(False),
    show_all: bool = Option(False, "--all"),
):
    table = Table(title="Mercado tools", header_style="bold magenta")

    @run_once
    def add_table_column(*args, **kwargs):
        table.add_column(*args, **kwargs)

    for _, tools in manager.get_supported_tools(separate_vendors=False):
        if verbose:
            table.add_section()

        for tool in tools:
            if filter_labels:
                if not any([label in tool.labels for label in filter_labels]):
                    continue

            exists = is_tool_available(tool)
            if not exists and not show_all:
                continue

            add_table_column("Name", style="bold")
            cells = [tool.name]

            if not names_only:
                add_table_column("Installed")
                cells.append(pretty_bool(exists))

                if verbose:
                    exists, is_latest, version, path, _ = manager.get_status(tool.name)
                    add_table_column("Is Latest")
                    cells.append(pretty_status(exists, is_latest))

                    add_table_column("Version")
                    cells.append(version)

                    add_table_column("Path")
                    cells.append(str(path))

                if with_labels:
                    add_table_column("Labels")
                    cells.append(",".join(map(lambda item: item.value, tool.labels)))

            table.add_row(*cells)

    console.print(table)


@app.command("install", help="Install a tool")
def install_tool(
    names: list[str],
    os: str = Option(get_host_operating_system()),
    arch: str = Option(get_host_architecture()),
    dry_run: bool = Option(False, envvar="DRY_RUN"),
):
    for name in names:
        installer = manager.get_installer(name, os, arch)
        logging.debug(f"'{installer.name}' was found with version '{installer.version}'")

        if not dry_run:
            logging.info(f"Installing '{installer.name}'...")
            installer.install()
            console.print(f":thumbs_up:\t'{name}' version {installer.version} is installed")


@app.command("uninstall", help="Uninstall a tool")
def uninstall_tool(
    names: list[str],
    dry_run: bool = Option(False, envvar="DRY_RUN"),
):
    for name in names:
        if not is_tool_available(manager.get_tool(name)):
            console.print(f":no_entry_sign:\t'{name}' could not be found.")
            continue

        logging.info(f"Uninstalling '{name}'...")

        if not dry_run:
            _, path = get_local_version(manager.get_tool(name))
            path.unlink()
            console.print(f":thumbs_up:\t'{name}' is uninstalled")


@app.command("is-latest", help="Check if the current version is the latest one")
def get_status(name: str):
    if not is_tool_available(manager.get_tool(name)):
        console.print(f":no_entry_sign:\t'{name}' could not be found.")
        raise Exit(code=1)

    _, is_latest, local_version, _, latest_version = manager.get_status(name)

    if not is_latest:
        console.print(f":thumbs_down:\t'{name}' version '{latest_version}' is available! (current: {local_version})")
        raise Exit(code=1)
    else:
        console.print(f":thumbs_up:\tYou have the latest version of '{name}' ({local_version})")


@app.command("show", help="Print information about the supported tool")
def show(name: str):
    exists, is_latest, local_version, path, latest_version = manager.get_status(name)

    console.print(f"Name: {name}")
    console.print(f"Status: {pretty_status(exists, is_latest)}")

    if exists:
        console.print(f"Local Version: {local_version}")
        console.print(f"Path: {path}")
    console.print(f"Remote Version: {latest_version}")


def init_logger(default_level: int = logging.INFO):
    loglevel = environ.get("LOGLEVEL", logging.getLevelName(default_level)).upper()
    logging.basicConfig(level=loglevel, format="%(message)s", handlers=[RichHandler(show_level=False, show_path=False)])


@app.callback()
def cli_logging(ctx: Context):
    if ctx.invoked_subcommand in ("show", "is-latest"):
        init_logger(logging.ERROR)
    else:
        init_logger(logging.INFO)


def main():
    try:
        app()
    except ValueError as ex:
        console.print(f":no_entry_sign:\t{ex}")
        exit(1)
