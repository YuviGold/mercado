
import platform

import pytest
from mercado.tool_manager import ToolManager

from mercado.vendors.github import GitHub
from mercado.vendors.hashicorp import Hashicorp
from mercado.vendors.vendor import ToolVendor


@pytest.fixture()
def os():
    yield platform.system().lower()


@pytest.fixture()
def arch():
    yield platform.machine()


@pytest.fixture()
def hashicorp() -> ToolVendor:
    yield Hashicorp()


@pytest.fixture()
def github() -> ToolVendor:
    yield GitHub()


@pytest.fixture()
def toolmanager() -> ToolManager:
    yield ToolManager()
