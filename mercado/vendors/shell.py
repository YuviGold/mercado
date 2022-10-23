import logging
import os
import subprocess
from dataclasses import dataclass, field
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Callable

from ..utils import INSTALL_DIR
from .vendor import Installer, Tool, ToolVendor


@dataclass(frozen=True)
class ShellTool(Tool):
    get_latest_version: Callable[[], str] = None
    download_script: Callable[[str], str] = None
    env_vars: dict[str, str] = field(default_factory=dict)


class Shell(ToolVendor):
    def get_latest_version(self, tool: ShellTool) -> str:
        return tool.get_latest_version()

    def get_installer(self, tool: ShellTool, version: str, *_) -> Installer:
        return ShellRunner(tool.name, version, tool.download_script, tool.env_vars)


class ShellRunner(Installer):
    def __init__(self, name: str, version: str, script: str, env: dict[str, str]):
        self.name = name
        self.version = version
        self._script = script
        self._env = env

    def install(self):
        script = dedent(self._script(self.version))
        logging.debug(f"Running {script}")
        with TemporaryDirectory() as tmp_dir:
            subprocess.check_call(script, env=self._env | {
                                  'PATH': f"{os.environ['PATH']}:{INSTALL_DIR}"}, shell=True, cwd=tmp_dir)
