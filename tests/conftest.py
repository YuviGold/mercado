import pytest
from mercado.tool_manager import ToolManager
from mercado.utils import get_host_architecture, get_host_operating_system
from mercado.vendors.github import GitHub
from mercado.vendors.hashicorp import Hashicorp
from mercado.vendors.vendor import ToolVendor


@pytest.fixture()
def os():
    yield get_host_operating_system()


@pytest.fixture()
def arch():
    yield get_host_architecture()


@pytest.fixture()
def hashicorp() -> ToolVendor:
    yield Hashicorp()


@pytest.fixture()
def github() -> ToolVendor:
    yield GitHub()


@pytest.fixture()
def toolmanager() -> ToolManager:
    yield ToolManager()
