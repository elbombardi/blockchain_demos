from brownie import config, network
import pytest
from scripts.utils import get_account
from scripts.deploy_and_create import deploy_and_create


def test_can_create_simple_collectible():
    if config["networks"][network.show_active()].get("local", False):
        pytest.skip

    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
