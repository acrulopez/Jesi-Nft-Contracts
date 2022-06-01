import pytest
from brownie import network, accounts
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
)


@pytest.fixture
def deploy_arguments():
    # [name, symbol, maxTotalSupply, collectionURI, mintFee]
    return ["collection_name", "collection_symbol", 3, "collection_uri", 0]


@pytest.fixture
def deploy_arguments_proxy():
    # [name, symbol, maxTotalSupply, collectionURI, mintFee]
    return ["proxy_name", "proxy_symbol", 2, "proxy_uri", 0]


@pytest.fixture
def skip_if_not_local():
    if (
        network.show_active()
        not in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS
    ):
        pytest.skip()
