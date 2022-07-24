import pytest
from brownie import (
    accounts,
    exceptions,
    Contract,
    Collection,
    CollectionManager,
    ERC1967Proxy,
)
from tests.conftest import skip_if_not_local, collection_arguments, deployments
from web3 import Web3
from scripts.helpful_scripts import get_from_config, encode_function_data
from scripts.deploy import deploy_collection_manager


def test_deploy_collection_manager(skip_if_not_local, deployments):

    (
        collection,
        collection_manager,
        collection_manager_proxy,
    ) = deployments

    assert collection_manager_proxy.collectionImplementation() == collection.address


def test_create_collection(skip_if_not_local, deployments, collection_arguments):
    account = accounts[0]
    (
        collection,
        collection_manager,
        collection_manager_proxy,
    ) = deployments

    with pytest.raises(exceptions.VirtualMachineError):
        assert collection_manager_proxy.collections(0)

    tx = collection_manager_proxy.createCollection(
        *collection_arguments, {"from": account}
    )
    tx.wait(1)

    collection_address = collection_manager_proxy.collections(0)
    assert collection_address is not None

    collection_proxy = Contract.from_abi(
        "Collection", collection_address, collection.abi
    )

    getters = [
        collection_proxy.name,
        collection_proxy.symbol,
        collection_proxy.description,
        collection_proxy.ipfsHash,
        collection_proxy.maxTotalSupply,
        collection_proxy.mintFee,
    ]
    for getter, value in zip(getters, collection_arguments):
        assert getter() == value


def test_non_free_mint(skip_if_not_local, deployments, collection_arguments):
    account = accounts[0]
    (
        collection,
        collection_manager,
        collection_manager_proxy,
    ) = deployments

    tx = collection_manager_proxy.createCollection(
        *collection_arguments, {"from": account}
    )
    tx.wait(1)

    collection_address = collection_manager_proxy.collections(0)
    collection_proxy = Contract.from_abi(
        "Collection", collection_address, collection.abi
    )

    mint_cost = collection_arguments[5]

    with pytest.raises(exceptions.VirtualMachineError):
        tx = collection_proxy.mint(account, "", {"from": account})
        tx.wait(1)

    with pytest.raises(exceptions.VirtualMachineError):
        tx = collection_proxy.mint(
            account, "", {"from": account, "value": mint_cost - 1}
        )
        tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        tx = collection_proxy.mint(
            account, "", {"from": account, "value": mint_cost + 1}
        )
        tx.wait(1)

    tx = collection_proxy.mint(account, "", {"from": account, "value": mint_cost})
    tx.wait(1)

    assert collection_proxy.ownerOf(0) == account
    assert collection_proxy.totalSupply() == 1


def test_transfer_from(skip_if_not_local, deployments, collection_arguments):

    account = accounts[0]
    account2 = accounts[1]
    account3 = accounts[2]
    (
        collection,
        collection_manager,
        collection_manager_proxy,
    ) = deployments

    tx = collection_manager_proxy.createCollection(
        *collection_arguments, {"from": account}
    )
    tx.wait(1)

    collection_address = collection_manager_proxy.collections(0)
    collection_proxy = Contract.from_abi(
        "Collection", collection_address, collection.abi
    )
    tx = collection_proxy.mint(
        account, "", {"from": account, "value": collection_arguments[5]}
    )

    # Act
    token_id = 0
    tx = collection_proxy.transferFrom(account, account2, token_id, {"from": account})
    tx.wait(1)

    assert collection_proxy.ownerOf(token_id) == account2

    tx = collection_proxy.transferFrom(account2, account3, token_id, {"from": account2})
    tx.wait(1)

    assert collection_proxy.ownerOf(token_id) == account3

    with pytest.raises(exceptions.VirtualMachineError):
        collection_proxy.safeTransferFrom(
            account2, account3, token_id, {"from": account2}
        )
