from brownie import SimpleCollectible
from scripts.utils import get_account

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"


def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(
        sample_token_uri,  {"from": account})
    tx.wait(1)
    print(
        f"Awsome you can view your NFT at {OPENSEA_FORMAT.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    print("Please wait up to 20 minutes, and hit the refresh metadata button.")
    return simple_collectible
