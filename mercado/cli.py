from typer import Option, Typer

from .tool_manager import ToolManager

app = Typer()


@app.command('list', help='List all available tools')
def list_products():
    manager = ToolManager()
    print(manager.get_supported_products())


@app.command('install', help='Install a tool')
def install_product(name: str,
                    dry_run: bool = Option(False, envvar='DRY_RUN')):
    manager = ToolManager()
    print(manager.get_release(name))


def main():
    app()
