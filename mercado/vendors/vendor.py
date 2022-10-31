from dataclasses import dataclass, field
from enum import Enum


class Label(Enum):
    K8S = "k8s"
    DOCS = "docs"
    SECURITY = "security"
    IAC = "iac"
    VCS = "vcs"
    VIRT = "virt"
    CICD = "ci/cd"


@dataclass(frozen=True)
class Tool:
    name: str
    labels: tuple[Label] = field(default_factory=tuple)


@dataclass
class Installer:
    name: str
    version: str

    def install(self):
        raise NotImplementedError()


class ToolVendor:
    def get_latest_version(self, tool: Tool) -> str:
        raise NotImplementedError()

    def get_installer(self, tool: Tool, version: str, os: str, arch: str) -> Installer:
        raise NotImplementedError()
