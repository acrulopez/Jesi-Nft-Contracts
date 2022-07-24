import pytest
from brownie import network, accounts
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
)
from scripts.deploy import deploy_collection_manager


@pytest.fixture
def deployments():
    return deploy_collection_manager()


@pytest.fixture
def collection_arguments():
    # [name, symbol, description, ipfsHash, maxTotalSupply, mintFee]
    return [
        "collection_name",
        "collection_symbol",
        "description",
        "hash on ipfs",
        5,
        1,
    ]


@pytest.fixture
def skip_if_not_local():
    if (
        network.show_active()
        not in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS
    ):
        pytest.skip()
