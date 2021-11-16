from scripts.utils import get_account, fund_link, get_oracle_contract
from brownie import APIConsumer, network, config
import time
from web3 import Web3


def deploy():
    account = get_account()
    jobId = bytes(config["networks"][network.show_active()]["jobId"], 'ascii')
    print(f"jobId {jobId}")
    fee = config["networks"][network.show_active()]["fee"]
    oracle = get_oracle_contract()
    print(f"Oracle contract {oracle} : {oracle.address}")
    #consumer = APIConsumer[-1]
    consumer = APIConsumer.deploy(oracle.address, jobId, fee, {
                                  "from": account}, publish_source=config["networks"][network.show_active()].get("verify", False))
    print(f"APIConsumer deployed {consumer}")
    fund_link(consumer.address)
    requestId = consumer.requestVolumeData({"from": account})
    print(f"Request Sent {requestId}")
    time.sleep(20)
    volume = consumer.volume()
    print(f"Volume == > {volume}")


def main():
    deploy()
