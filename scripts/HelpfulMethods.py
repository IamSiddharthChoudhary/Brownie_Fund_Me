from decimal import Decimal
from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMAL = 8
STARTING_PRICE = 2000
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev", "mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "jatt"]


def getAccount():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    else:
        return accounts.add(config["wallets"]["from_key"])


def deployMocks():
    if network.show_active() not in FORKED_LOCAL_ENVIRONMENTS:
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(DECIMAL, 2000 * 10**8, {"from": getAccount()})
