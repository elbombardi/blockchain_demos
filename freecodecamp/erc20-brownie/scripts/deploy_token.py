from brownie import DonationToken, accounts
from scripts.utils import get_account
from web3 import Web3


def main():
    deploy()


def deploy():
    account = get_account()
    initialSupply = Web3.toWei(1000_000_000_000, "ether")
    donationToken = DonationToken.deploy(initialSupply, {"from": account})
    print(
        f"""Donnation Token is deployed at the address {donationToken.address} 
        The initial supply is {Web3.fromWei(donationToken.balanceOf(account.address), 'ether')} DON """)
