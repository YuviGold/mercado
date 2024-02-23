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
    download_script: Callable[[str, str, str], str] = None
    env_vars: dict[str, str] = field(default_factory=dict)


class Shell(ToolVendor):
    def get_latest_version(self, tool: ShellTool) -> str:
        return tool.get_latest_version()

    def get_installer(self, tool: ShellTool, version: str, os: str, arch: str) -> Installer:
        return ShellRunner(tool.name, version, os, arch, tool.download_script, tool.env_vars)


class ShellRunner(Installer):
    def __init__(
        self, name: str, version: str, os: str, arch: str, script: Callable[[str, str, str], str], env: dict[str, str]
    ):
        self.name = name
        self.version = version
        self.os = os
        self.arch = arch
        self._script = script
        self._env = env

    def install(self):
        script = "set -o errexit"
        script += dedent(self._script(self.version, self.os, self.arch))
        with TemporaryDirectory() as tmp_dir:
            logging.debug(f"Running the following script in {tmp_dir}:\n{script}")
            subprocess.check_call(
                script, env=self._env | {"PATH": f"{os.environ['PATH']}:{INSTALL_DIR}"}, shell=True, cwd=tmp_dir
            )
