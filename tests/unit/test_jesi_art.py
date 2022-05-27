import pytest
from brownie import accounts, JesiArt, exceptions
from tests.conftest import skip_if_not_local


def test_transfer_from(skip_if_not_local):
    account = accounts[0]
    account2 = accounts[1]
    account3 = accounts[2]
    jesi_art = JesiArt.deploy("Jesi Art", "JES", 100, {"from": account})

    tx = jesi_art.mint(account, "", {"from": account})
    tx.wait(1)
    token_id = tx.return_value

    tx = jesi_art.safeTransferFrom(account, account2, 0)
    tx.wait(1)

    assert jesi_art.ownerOf(token_id) == account2


def test_burn(skip_if_not_local):
    account = accounts[0]
    account2 = accounts[1]
    account3 = accounts[2]
    jesi_art = JesiArt.deploy("Jesi Art", "JES", 100, {"from": account})

    tx = jesi_art.mint(account, "", {"from": account})
    tx.wait(1)
    token_id = tx.return_value

    with pytest.raises(exceptions.VirtualMachineError):
        tx = jesi_art.burn(token_id, {"from": account2})

    tx = jesi_art.burn(token_id, {"from": account})
    tx.wait(1)

    assert jesi_art.totalSupply() == 0
    with pytest.raises(exceptions.VirtualMachineError):
        jesi_art.ownerOf(token_id)
