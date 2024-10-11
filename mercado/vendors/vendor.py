from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Label(Enum):
    DOCS = "docs"
    SECURITY = "security"
    IAC = "iac"
    VCS = "vcs"
    VIRT = "virt"
    CICD = "ci/cd"
    STORAGE = "storage"
    NETWORK = "network"
    ORCHESTRATE = "orchestration"
    CLOUD = "cloud"

    DOCKER = "docker"
    K8S = "k8s"


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
