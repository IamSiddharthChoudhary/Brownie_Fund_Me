from brownie import Funds, MockV3Aggregator, network, config
from scripts.HelpfulMethods import (
    getAccount,
    deployMocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deployFundMe():
    account = getAccount()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        priceFeed = config["networks"][network.show_active()]["eth_usd_price_feed"]

    else:
        deployMocks()
        priceFeed = MockV3Aggregator[-1].address

    fundMe = Funds.deploy(
        priceFeed,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"The contract deployed to {fundMe.address}")
    return fundMe


def main():
    deployFundMe()
