from dataclasses import dataclass, field
from enum import StrEnum, auto
from pathlib import Path


class Label(StrEnum):
    DOCS = auto()
    SECURITY = auto()
    IAC = auto()
    VCS = auto()
    VIRT = auto()
    CICD = auto()
    STORAGE = auto()
    NETWORK = auto()
    ORCHESTRATE = auto()
    CLOUD = auto()
    BUILD = auto()

    DOCKER = auto()
    K8S = auto()


@dataclass(frozen=True)
class Tool:
    name: str
    labels: tuple[Label, ...] = field(default_factory=tuple)
    target: Path = None


@dataclass
class Installer:
    name: str
    version: str

    def install(self):
        raise NotImplementedError


class ToolVendor:
    def get_latest_version(self, tool: Tool) -> str:
        raise NotImplementedError

    def get_installer(self, tool: Tool, version: str, os: str, arch: str) -> Installer:
        raise NotImplementedError
