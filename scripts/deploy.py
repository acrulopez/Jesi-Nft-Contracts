from scripts.helpful_scripts import get_account, get_from_config, encode_function_data
from brownie import JesiArt, ProxyAdmin, TransparentUpgradeableProxy, Contract


def deploy_jesi_art(name, token, max_tokens):
    account = get_account()
    jesi_art = JesiArt.deploy(
        name,
        token,
        max_tokens,
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    return jesi_art.address


def deploy_collection(name, token, max_tokens):
    account = get_account()
    jesi_art = (
        JesiArt.deploy(
            name,
            token,
            max_tokens,
            {"from": account},
            publish_source=get_from_config("verify", False),
        )
        if len(JesiArt) == 0
        else JesiArt[-1]
    )

    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    initializer = (jesi_art.initialize, name, token, max_tokens)

    proxy = TransparentUpgradeableProxy.deploy(
        jesi_art.address,
        proxy_admin.address,
        encode_function_data(*initializer),
        {"from": account, "gas_limit": 1000000},
        publish_source=get_from_config("verify", False),
    )

    # proxy_jesi_art = Contract.from_abi("Jesi Art", proxy.address, jesi_art.abi)

    return {
        "proxy_admin": proxy_admin.address,
        "proxy_collection": proxy.address,
    }


# def main(name, token, max_tokens):
#     deploy_new_collection(name, token, max_tokens)
