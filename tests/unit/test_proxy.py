from scripts.helpful_scripts import (
    get_account,
    get_from_config,
    encode_function_data,
    upgrade,
)
from brownie import (
    JesiArt,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    UpgradedJesiArt,
    exceptions,
)

import pytest


def test_proxy():

    NAME = "Jesi's generative art"
    TOKEN = "JESIART"
    MAX_TOKENS = 50

    account = get_account()
    jesi_art = JesiArt.deploy(
        "foo",
        "foo",
        5,
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    initializer = (jesi_art.initialize, NAME, TOKEN, MAX_TOKENS)

    proxy = TransparentUpgradeableProxy.deploy(
        jesi_art.address,
        proxy_admin.address,
        encode_function_data(*initializer),
        {"from": account, "gas_limit": 1000000},
        publish_source=get_from_config("verify", False),
    )

    proxy_jesi_art = Contract.from_abi("Jesi Art", proxy.address, jesi_art.abi)

    assert proxy_jesi_art.name() == NAME
    assert proxy_jesi_art.symbol() == TOKEN
    assert proxy_jesi_art.maxTotalSupply() == MAX_TOKENS
    assert jesi_art.name() == "foo"

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_jesi_art.initialize("a", "a", 1, {"from": account})

    # Upgrade contract
    upgraded_jesi_art = UpgradedJesiArt.deploy(
        "foo2",
        "foo2",
        6,
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    upgrade(account, proxy, upgraded_jesi_art.address, proxy_admin)
    proxy_upgraded_jesi_art = Contract.from_abi(
        "Upgraded Jesi Art", proxy.address, upgraded_jesi_art.abi
    )

    assert proxy_upgraded_jesi_art.foo() == 0
    proxy_upgraded_jesi_art.setFoo(24, {"from": account})
    assert proxy_upgraded_jesi_art.foo() == 24

    assert proxy_upgraded_jesi_art.name() == NAME
    assert proxy_upgraded_jesi_art.symbol() == TOKEN
    assert proxy_upgraded_jesi_art.maxTotalSupply() == MAX_TOKENS
    assert jesi_art.name() == "foo"

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_upgraded_jesi_art.initialize("a", "a", 1, {"from": account})
