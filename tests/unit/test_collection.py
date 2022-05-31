import pytest
from brownie import accounts, Collection, exceptions
from tests.conftest import skip_if_not_local


def test_transfer_from(skip_if_not_local):
    account = accounts[0]
    account2 = accounts[1]
    account3 = accounts[2]
    collection = Collection.deploy("Jesi Art", "JES", 100, "uri", {"from": account})

    tx = collection.mint(account, "", {"from": account})
    tx.wait(1)
    token_id = tx.return_value

    tx = collection.safeTransferFrom(account, account2, 0)
    tx.wait(1)

    assert collection.ownerOf(token_id) == account2


def test_burn(skip_if_not_local):
    account = accounts[0]
    account2 = accounts[1]
    account3 = accounts[2]
    collection = Collection.deploy("Jesi Art", "JES", 100, "uri", {"from": account})

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
