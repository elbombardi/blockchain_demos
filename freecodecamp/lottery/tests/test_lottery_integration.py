from brownie import config, network
import pytest
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import fund_with_link, get_account
import time


def test_can_pick_winner():
    if config["networks"][network.show_active()].get("local"):
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    print(f"Lottery Balance : {lottery.balance()}")
    lottery.endLottery({"from": account})
    time.sleep(60)
    assert lottery.winner() == account
    assert lottery.balance == 0
