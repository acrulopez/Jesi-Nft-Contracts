from scripts.helpful_scripts import get_account, get_from_config, encode_function_data
from brownie import Collection, CollectionManager, ERC1967Proxy, Contract, accounts


def deploy_collection_manager():
    """Deploy the Collection implementation contract, the CollectionManager
    implementation contract and the proxy for the CollectionManager.

    Returns:
        str: address of the new contract
    """
    account = get_account()

    # Deploy collection implementation
    collection = Collection.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    # Deploy collection manager implementation
    collection_manager = CollectionManager.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    # Deploy collection manager proxy
    collection_manager_proxy = ERC1967Proxy.deploy(
        collection_manager.address,
        encode_function_data(
            collection_manager.initialize, collection.address, account
        ),
        {"from": account},
        publish_source=get_from_config("verify", False),
    )
    collection_manager_proxy = Contract.from_abi(
        "Collection Manager", collection_manager_proxy.address, collection_manager.abi
    )

    return collection, collection_manager, collection_manager_proxy


def main():
    deploy_collection_manager()
