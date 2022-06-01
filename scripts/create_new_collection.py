from scripts.deploy import deploy_collection_w_proxy
from scripts.ipfs_scripts import local_directory_to_ipfs, json_to_ipfs
from bullet import Input, Numbers
import os
import json
from brownie import network
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
)


def create_new_collection(collection_filename):
    """Create a new collection from a file on ./collections and
    overwrites it with the new information of the contract

    Args:
        collection_filename (str): Json filename on folder ./collections . Ex: swifty-grid.json

    Raises:
        Exception: If the file does not exists on ./collections
        Exception: If the collection is already deployed in a non-local environment
    """

    collection_path = f"./collections/{collection_filename}"

    # Check the file exists
    if not os.path.exists(collection_path):
        raise Exception(f"The file {collection_path} does not exist")

    # Opens the file
    with open(collection_path, "r") as f:
        collection_json = json.load(f)

    # Check the collection is not deployed
    if "proxy_admin" in collection_json:
        raise Exception(f"The collection is already deployed. See {collection_path}")

    # Read properties
    name = collection_json["name"]
    token = collection_json["token"]
    max_supply = collection_json["maxSupply"]
    generativeUri = collection_json["generativeUri"]
    mintFee = collection_json["mintFee"]

    # Upload generative art to IPFS and set it on collection_json
    generativeUri = local_directory_to_ipfs(generativeUri)
    collection_json["generativeUri"] = generativeUri

    # TODO upload thumbnail
    # collection_json["thumbnailUri"] = thumbnailUri

    # Upload collection json to IPFS
    collectionUri = json_to_ipfs(collection_json)
    proxy_addresses_json = deploy_collection_w_proxy(
        name, token, max_supply, collectionUri, mintFee
    )
    collection_json.update(proxy_addresses_json)

    # Write on folder 'local' if deploying in a local environment
    if (
        network.show_active()
        in FORKED_LOCAL_ENVIRONMENTS + LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        collection_path = f"./collections/local/{collection_filename}"
        os.makedirs(os.path.dirname(collection_path), exist_ok=True)

    # Write the new updated file
    with open(collection_path, "w") as f:
        json.dump(collection_json, f)
