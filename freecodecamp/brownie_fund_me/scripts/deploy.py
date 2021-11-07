from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks


def deploy_fund_me():
    account = get_account()

    if config["networks"][network.show_active()].get("deploy_mocks"):
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    else:
        price_feed_address = config["networks"][network.show_active(
        )]["eth_usd_price_feed"]

    fund_me = FundMe.deploy(price_feed_address, {"from": account},
                            publish_source=config["networks"][network.show_active()].get("verify"))

    print(f"Contract deployed to {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
