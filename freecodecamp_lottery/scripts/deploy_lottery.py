from brownie import Lottery, config, network
from scripts.utils import get_account, get_contract, fund_with_link
import time


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify", False)
    )
    return lottery
    print("Deployed Lottery!")


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("Lottery started")


def end_lottery():
    print(f"Ending the lottery...")
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx2 = lottery.endLottery({"from": account})
    tx2.wait(1)
    time.sleep(60)
    print(f"{lottery.winner()} is the winner of the lottery")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery")
