import pytest
from mercado.vendors.hashicorp import Hashicorp
from mercado.vendors.vendor import Tool


def test_get_latest_release_invalid_tool(hashicorp: Hashicorp):
    with pytest.raises(ValueError):
        hashicorp._get_hashicorp_latest_release(Tool("invalid"))
