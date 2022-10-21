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


@dataclass
class Artifact:
    name: str
    os: str
    arch: str
    version: str = ''
    url: str = ''


@dataclass
class Tool:
    name: str
    labels: list[Label] = field(default_factory=list)


class ToolVendor:
    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()

    def get_latest_release(self, tool: Tool, os: str, arch: str) -> Artifact:
        raise NotImplementedError()

    def get_release_by_version(self, tool: Tool, version: str, os: str, arch: str) -> Artifact:
        raise NotImplementedError()
