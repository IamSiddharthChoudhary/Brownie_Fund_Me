from scripts.HelpfulMethods import getAccount, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deployFundMe
from brownie import accounts, network, exceptions
import pytest


def testFundMe():
    account = getAccount()
    fundMe = deployFundMe()
    entranceFee = fundMe.getEntraceFees() + 100
    tx = fundMe.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert fundMe.fundsArray(account.address) == entranceFee
    tx1 = fundMe.withdraw({"from": account})
    tx1.wait(1)
    assert fundMe.fundsArray(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund = deployFundMe()
    badActor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund.withdraw({"from": badActor})
