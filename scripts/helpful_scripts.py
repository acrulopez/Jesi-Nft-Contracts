from brownie import network, accounts, config
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
IPFS_IMAGE_URL = "https://ipfs.io/ipfs/{}"


def get_account(index=None, id=None):
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
    if return_value_if_not_exist is not None:
        return config["networks"][network.show_active()].get(
            key, return_value_if_not_exist
        )
    else:
        return config["networks"][network.show_active()][key]


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or initializer == None:
        return eth_utils.to_bytes(hexstr="0x")
    else:
        print(*args)
        return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin=None,
    initializer=None,
    *args
):
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
