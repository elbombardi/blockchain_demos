
from brownie import Contract, accounts, config, network, MockV3Aggregator, VRFCoordinatorMock, LinkToken

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}


def get_contract(contract_name):
    """This function will grab the contract addresses from brownie config, or will deploy a mock version
        Args :
            contract_name (string)

        returns
            brownie.network.contract.ProjectContract: the most recently deployed version of the contract
    """
    contract_type = contract_to_mock[contract_name]
    if config["networks"][network.show_active()].get("deploy_mocks"):
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi)
    return contract


DECIMALS = 8
DEFAULT_VALUE = 200_000_000_000


def deploy_mocks(decimals=DECIMALS, initial_value=DEFAULT_VALUE):
    print(f"The active network is {network.show_active()}")
    print("Deploying mock for AggregatorV3Interface")
    account = get_account()
    MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account})
    print("Deploying mock for LinkToken")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying mock for VRFCoordinator")
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks deployed")


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if config["networks"][network.show_active()].get("local"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def fund_with_link(contract_address, account=None, link_token=None, amount=200000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded with Link")
    return tx
