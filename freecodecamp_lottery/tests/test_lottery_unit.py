from brownie import config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import get_account, fund_with_link, get_contract
import pytest

LOTTERY_STATE_OPEN = 0
LOTTERY_STATE_CLOSED = 1
LOTTERY_STATE_CALCULATING_WINNER = 2


def test_get_entrance_fee():
    if not config["networks"][network.show_active()].get("local"):
        pytest.skip()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = 0.025 * 10**18
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    if not config["networks"][network.show_active()].get("local"):
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter(
            {"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if not config["networks"][network.show_active()].get("local"):
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account


def test_can_end_lottery():
    if not config["networks"][network.show_active()].get("local"):
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.getLotteryState() == LOTTERY_STATE_CALCULATING_WINNER


def test_can_pick_winner_correctly():
    if not config["networks"][network.show_active()].get("local"):
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    tx = lottery.endLottery({"from": account})
    request_id = tx.events["RequestRandomness"]["requestId"]
    vrfCoordinator = get_contract("vrf_coordinator")
    STATIC_RANGE = 777
    starting_account_balance = account.balance()
    lottery_balance = lottery.balance()
    vrfCoordinator.callBackWithRandomness(
        request_id, STATIC_RANGE, lottery.address, {"from": account})
    assert lottery.winner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_account_balance + lottery_balance
