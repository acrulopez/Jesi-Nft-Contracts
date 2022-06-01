import pytest
from brownie import (
    accounts,
    Collection,
    exceptions,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)
from tests.conftest import skip_if_not_local, deploy_arguments
from web3 import Web3
from scripts.helpful_scripts import get_from_config, encode_function_data


def test_withdraw(skip_if_not_local, deploy_arguments):

    account = accounts[0]
    account2 = accounts[1]

    collection = Collection.deploy(
        *deploy_arguments,
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    mint_cost = Web3.toWei(0.1, "ether")
    deploy_arguments[4] = mint_cost  # Set the price to mint to 0.1
    initializer = (collection.initialize, *deploy_arguments)

    proxy = TransparentUpgradeableProxy.deploy(
        collection.address,
        proxy_admin.address,
        encode_function_data(*initializer),
        {"from": account, "gas_limit": 1000000},
        publish_source=get_from_config("verify", False),
    )

    proxy_collection = Contract.from_abi("Jesi Art", proxy.address, collection.abi)

    tx = proxy_collection.mint(account, "", {"from": account2, "value": mint_cost})
    tx.wait(1)
    tx = proxy_collection.mint(account, "", {"from": account2, "value": mint_cost})
    tx.wait(1)

    with pytest.raises(exceptions.VirtualMachineError):
        tx = proxy_collection.withdraw({"from": account2})
        tx.wait(1)

    initial_balance = account.balance()
    tx = proxy_collection.withdraw({"from": account})
    tx.wait(1)

    assert account.balance() >= initial_balance


def test_non_free_mint(skip_if_not_local, deploy_arguments):
    account = accounts[0]
    account2 = accounts[1]

    mint_cost = Web3.toWei(0.1, "ether")
    deploy_arguments[4] = mint_cost  # Set the price to mint to 0.1
    collection = Collection.deploy(*deploy_arguments, {"from": account})

    with pytest.raises(exceptions.VirtualMachineError):
        tx = collection.mint(account, "", {"from": account})
        tx.wait(1)

    with pytest.raises(exceptions.VirtualMachineError):
        tx = collection.mint(account, "", {"from": account, "value": mint_cost - 1})
        tx.wait(1)

    tx = collection.mint(account, "", {"from": account, "value": mint_cost})
    tx.wait(1)
    token_id0 = tx.return_value

    assert token_id0 == 0
    assert collection.ownerOf(token_id0) == account
    assert collection.totalSupply() == 1


def test_free_mint(skip_if_not_local, deploy_arguments):

    account = accounts[0]
    account2 = accounts[1]
    account3 = accounts[3]
    collection = Collection.deploy(*deploy_arguments, {"from": account})

    tx = collection.mint(account, "", {"from": account})
    tx.wait(1)
    token_id0 = tx.return_value

    assert token_id0 == 0
    assert collection.ownerOf(token_id0) == account

    tx = collection.mint(account, "", {"from": account2})
    tx.wait(1)
    token_id1 = tx.return_value

    assert token_id1 == 1
    assert collection.ownerOf(token_id1) == account
    assert collection.totalSupply() == 2

    tx = collection.mint(
        account3,
        "",
        {"from": account2, "value": Web3.toWei(0.1, "ether")},
    )
    tx.wait(1)
    token_id2 = tx.return_value

    assert token_id2 == 2
    assert collection.ownerOf(token_id2) == account3
    assert collection.totalSupply() == 3


def test_transfer_from(skip_if_not_local, deploy_arguments):

    account = accounts[0]
    account2 = accounts[1]
    account3 = accounts[2]
    collection = Collection.deploy(*deploy_arguments, {"from": account})

    tx = collection.mint(account, "", {"from": account})
    tx.wait(1)
    token_id = tx.return_value

    tx = collection.transferFrom(account, account2, token_id, {"from": account})
    tx.wait(1)

    assert collection.ownerOf(token_id) == account2

    tx = collection.transferFrom(account2, account3, token_id, {"from": account2})
    tx.wait(1)

    assert collection.ownerOf(token_id) == account3

    with pytest.raises(exceptions.VirtualMachineError):
        collection.safeTransferFrom(account2, account3, token_id, {"from": account2})


def test_burn(skip_if_not_local, deploy_arguments):
    account = accounts[0]
    account2 = accounts[1]
    collection = Collection.deploy(*deploy_arguments, {"from": account})

    tx = collection.mint(account, "", {"from": account})
    tx.wait(1)
    token_id = tx.return_value

    with pytest.raises(exceptions.VirtualMachineError):
        tx = collection.burn(token_id, {"from": account2})

    tx = collection.burn(token_id, {"from": account})
    tx.wait(1)

    assert collection.totalSupply() == 0
    with pytest.raises(exceptions.VirtualMachineError):
        collection.ownerOf(token_id)
