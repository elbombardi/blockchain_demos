from brownie import network, config, accounts, exceptions
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.getAmountFundedFromAddress(account.address) == entrance_fee
    tx = fund_me.withdraw({"from": account})
    tx.wait(1)
    assert fund_me.getAmountFundedFromAddress(account.address) == 0


def test_only_owner_can_withdraw():
    if config["networks"][network.show_active()].get("local") != True:
        pytest.skip("only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
