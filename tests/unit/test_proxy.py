from scripts.helpful_scripts import (
    get_account,
    get_from_config,
    encode_function_data,
    upgrade,
)
from brownie import (
    Collection,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    UpgradedCollection,
    exceptions,
)

from tests.conftest import deploy_arguments, deploy_arguments_proxy

import pytest


def test_proxy(deploy_arguments, deploy_arguments_proxy):

    account = get_account()
    collection = Collection.deploy(
        *deploy_arguments,
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    initializer = (collection.initialize, *deploy_arguments_proxy)

    proxy = TransparentUpgradeableProxy.deploy(
        collection.address,
        proxy_admin.address,
        encode_function_data(*initializer),
        {"from": account, "gas_limit": 1000000},
        publish_source=get_from_config("verify", False),
    )

    proxy_collection = Contract.from_abi("Jesi Art", proxy.address, collection.abi)

    assert proxy_collection.name() == deploy_arguments_proxy[0]
    assert proxy_collection.symbol() == deploy_arguments_proxy[1]
    assert proxy_collection.maxTotalSupply() == deploy_arguments_proxy[2]
    assert proxy_collection.collectionURI() == deploy_arguments_proxy[3]
    assert collection.name() == deploy_arguments[0]

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_collection.initialize(*deploy_arguments, {"from": account})

    # Upgrade contract
    upgraded_jesi_art = UpgradedCollection.deploy(
        *deploy_arguments_proxy,
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

    assert proxy_upgraded_jesi_art.name() == deploy_arguments_proxy[0]
    assert proxy_upgraded_jesi_art.symbol() == deploy_arguments_proxy[1]
    assert proxy_upgraded_jesi_art.maxTotalSupply() == deploy_arguments_proxy[2]
    assert proxy_upgraded_jesi_art.collectionURI() == deploy_arguments_proxy[3]
    assert collection.name() == deploy_arguments[0]

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_upgraded_jesi_art.initialize(*deploy_arguments, {"from": account})
