from brownie import accounts, config, network


def get_account():
    if config["networks"][network.show_active()].get("local"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
