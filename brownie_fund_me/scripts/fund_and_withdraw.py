from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"Entrance fee : {entrance_fee}")
    print("Funding...")
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    print("Withdrawing")
    tx = fund_me.withdraw({"from": account})
    tx.wait(1)


def main():
    fund()
    withdraw()
