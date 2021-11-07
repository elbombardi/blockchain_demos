from brownie import network, accounts, config, MockV3Aggregator


def get_account():
    if config["networks"][network.show_active()].get("local"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    if len(MockV3Aggregator) <= 0:
        print("Deploying mocks")
        MockV3Aggregator.deploy(
            8, 200_000_000_000, {"from": get_account()})
        print("Mocks deployed")
