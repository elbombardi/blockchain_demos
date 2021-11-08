
from brownie import config, accounts, network


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if config["networks"][network.show_active()].get("local"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
