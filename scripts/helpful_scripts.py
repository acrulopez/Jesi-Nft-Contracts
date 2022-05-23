from brownie import network, accounts, config

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
