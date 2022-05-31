from brownie import network, accounts, config
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
IPFS_IMAGE_URL = "https://ipfs.io/ipfs/{}"
PINATA_IPFS_GATEWAY = "https://gateway.pinata.cloud/ipfs/{}"
PINATA_PIN_FILE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
PINATA_PIN_JSON_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"


def get_account(index=None, id=None):
    """Get an account to interact with the blockchain. If it's a local
    deployment, it will take accounts[0 or index if index is not None].
    Otherwise it will take it from the private key set on the configuration.

    Args:
        index (_type_, optional): _description_. Defaults to None.
        id (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif (
        network.show_active()
        in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_from_config(key, return_value_if_not_exist=None):
    """Get a value from the configuration

    Args:
        key (str): Value that want to be retrieved
        return_value_if_not_exist (any, optional): Value that should be returned if key
            not in configuration. Defaults to None.

    Returns:
        str: Value corresponding to the key provided
    """
    if return_value_if_not_exist is not None:
        return config["networks"][network.show_active()].get(
            key, return_value_if_not_exist
        )
    else:
        return config["networks"][network.show_active()][key]


def encode_function_data(initializer=None, *args):
    """Encode the data of a function and its arguments so it
    can be called as calldata

    Args:
        initializer (_type_, optional): _description_. Defaults to None.

    Returns:
        bytes: Bytes of the initializer and its arguments encoded
    """
    if len(args) == 0 or initializer == None:
        return eth_utils.to_bytes(hexstr="0x")
    else:
        return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin=None,
    initializer=None,
    *args
):
    """Upgrade an existing contract for a new one

    Args:
        account (brownie.Account): Account to send the transaction from
        proxy (brownie.Contract): Proxy contract
        new_implementation_address (str): Address of the new contract
        proxy_admin (brownie.Contract, optional): Contract of the proxy_admin. Defaults to None.
        initializer (bytes, optional): Initializer of the new contract if needed. Defaults to None.
        *args: Arguments for the initializer

    Returns:
        brownie.Transaction: Transaction corresponding to the upgrade of the contract
    """
    transaction = None
    if proxy_admin:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account, "gas_limit": 1000000},
            )
        else:
            transaction = proxy_admin.upgrade(
                proxy.address,
                new_implementation_address,
                {"from": account, "gas_limit": 1000000},
            )

    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address,
                encoded_function_call,
                {"from": account, "gas_limit": 1000000},
            )
        else:
            transaction = proxy.upgradeTo(
                new_implementation_address,
                {"from": account, "gas_limit": 1000000},
            )

    return transaction
