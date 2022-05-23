from scripts.helpful_scripts import get_account, get_from_config
from brownie import JesiArt

NAME = "Jesi's generative art"
TOKEN = "JESIART"


def deploy_contract():
    account = get_account()
    jesi_ntf_art = JesiArt.deploy(
        NAME, TOKEN, {"from": account}, publish_source=get_from_config("verify", False)
    )


def main():
    deploy_contract()
