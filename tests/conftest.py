import pytest

from mercado.tool_manager import ToolManager
from mercado.utils import get_host_architecture, get_host_operating_system
from mercado.vendors.github import GitHub
from mercado.vendors.hashicorp import Hashicorp
from mercado.vendors.vendor import ToolVendor


@pytest.fixture
def os():
    return get_host_operating_system()


@pytest.fixture
def arch():
    return get_host_architecture()


@pytest.fixture
def hashicorp() -> ToolVendor:
    return Hashicorp()


@pytest.fixture
def github() -> ToolVendor:
    return GitHub()


@pytest.fixture
def toolmanager() -> ToolManager:
    return ToolManager()
