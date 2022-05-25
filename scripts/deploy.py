from scripts.helpful_scripts import get_account, get_from_config, encode_function_data
from brownie import JesiArt, ProxyAdmin, TransparentUpgradeableProxy, Contract

NAME = "Jesi's generative art"
TOKEN = "JESIART"
MAX_TOKEN = 50


def deploy_contract():
    account = get_account()
    jesi_art = JesiArt.deploy(
        NAME,
        TOKEN,
        MAX_TOKEN,
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=get_from_config("verify", False),
    )

    initializer = (jesi_art.initialize, NAME, TOKEN, MAX_TOKEN)

    proxy = TransparentUpgradeableProxy.deploy(
        jesi_art.address,
        proxy_admin.address,
        encode_function_data(*initializer),
        {"from": account, "gas_limit": 1000000},
        publish_source=get_from_config("verify", False),
    )

    proxy_jesi_art = Contract.from_abi("Jesi Art", proxy.address, jesi_art.abi)

    print("----------------", proxy_jesi_art.name())

    return jesi_art, proxy_admin, proxy, proxy_jesi_art


def main():
    deploy_contract()
