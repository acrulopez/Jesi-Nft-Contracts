from scripts.helpful_scripts import get_account, get_from_config, encode_function_data
from brownie import Collection, ProxyAdmin, TransparentUpgradeableProxy


def deploy_collection(name, token, max_supply, ipfs_uri, mint_fee):
    """Deploy the Collection contract

    Args:
        name (str): Name of the ERC721 token
        token (str): Token of the ERC721
        max_supply (uint): Maximum number of tokens that can be minted
        ipfs_uri (str): URI of the generative art root in IPFS
        mint_fee (int): Fee to be able to mint a new token

    Returns:
        str: address of the new contract
    """
    account = get_account()
    collection = Collection.deploy(
        name,
        token,
        max_supply,
        ipfs_uri,
        mint_fee,
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    return collection


def deploy_collection_w_proxy(name, token, max_supply, ipfs_uri, mint_fee):
    """Deploy a collection using the latest Collection contract.
    This will deploy the proxya and the proxy_admin

    Args:
        name (str): Name of the ERC721 token
        token (str): Token of the ERC721
        max_supply (uint): Maximum number of tokens that can be minted
        ipfs_uri (str): URI of the generative art root in IPFS
        mint_fee (int): Fee to be able to mint a new token

    Returns:
        dict: json containing the address of the proxy and the proxy_admin
    """
    account = get_account()

    # Deploy a Collection contract if there are none deployed
    collection = (
        deploy_collection(name, token, max_supply, ipfs_uri, mint_fee)
        if len(Collection) == 0
        else Collection[-1]
    )

    # Deploy the proxy_admin
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    # Create the initializer and deploy the proxy
    initializer = (collection.initialize, name, token, max_supply, ipfs_uri, mint_fee)
    proxy = TransparentUpgradeableProxy.deploy(
        collection.address,
        proxy_admin.address,
        encode_function_data(*initializer),
        {"from": account, "gas_limit": 1000000},
        publish_source=get_from_config("verify", False),
    )

    return {
        "proxy_admin": proxy_admin.address,
        "proxy_contract": proxy.address,
    }
