from brownie import config, network, accounts, LinkToken, Contract, MockOracle
from web3 import Web3


def get_account():
    if config["networks"][network.show_active()].get("local", False):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_link_token():
    if config["networks"][network.show_active()].get("mock", False):
        return get_mock_contract(LinkToken)
    else:
        link_token_address = config["networks"][network.show_active(
        )]["link_token"]
        return get_real_contract(link_token_address, LinkToken)


def get_oracle_contract():
    if config["networks"][network.show_active()].get("mock", False):
        return get_mock_contract(MockOracle)
    else:
        oracle_address = config["networks"][network.show_active(
        )]["oracle"]
        return get_real_contract(oracle_address, MockOracle)


def get_mock_contract(contract_type):
    account = get_account()
    if len(contract_type) == 0:
        contract_type.deploy({"from": account})
    return contract_type[-1]


def get_real_contract(address, contract_type):
    return Contract.from_abi(contract_type._name, address, contract_type.abi)


def fund_link(address):
    account = get_account()
    linkToken = get_link_token()
    amount = config["networks"][network.show_active()]["fee"]
    print(
        f"Transferting {Web3.fromWei(amount, 'ether')} Link to contract address")
    tx = linkToken.transfer(address, amount, {"from": account})
    tx.wait(1)
