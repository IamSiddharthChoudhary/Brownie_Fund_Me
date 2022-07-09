from brownie import Funds
from scripts.HelpfulMethods import getAccount


def fund():
    fundMe = Funds[-1]
    account = getAccount()
    entranceFee = fund.getEntraceFees()
    print(entranceFee)
    print(f"The current entry fees is {entranceFee}")
    # All the low level data in transaction to function calls will be from here
    fundMe.fund({"from": account, "value": entranceFee})


def withdraw():
    fundMe = Funds[-1]
    account = getAccount()
    fundMe.withdraw({"from": account})


def main():
    fund()
    withdraw()
