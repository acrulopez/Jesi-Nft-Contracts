import os
import requests
import sys
from scripts.helpful_scripts import (
    IPFS_IMAGE_URL,
    PINATA_PIN_FILE_URL,
    PINATA_PIN_JSON_URL,
    PINATA_IPFS_GATEWAY,
)
import os
import json


# Headers for the post call to pinata
HEADERS = {
    "pinata_api_key": os.environ["PINATA_API_KEY"],
    "pinata_secret_api_key": os.environ["PINATA_SECRET_API_KEY"],
}


def json_to_ipfs(dict_like_json):
    """Upload a dict like json to IPFS

    Args:
        dict_like_json (dict): Dict to upload to IPFS

    Raises:
        Exception: If dict_like_json is not a dictionary

    Returns:
        str: URI on IPFS of the uploaded json
    """

    if type(dict_like_json) != dict:
        raise Exception(
            f"The input of 'json_to_ipfs' function should be a dictionary. Sent type: {type(dict_like_json)}"
        )

    final_json = {"pinataContent": dict_like_json}

    response = requests.post(
        PINATA_PIN_JSON_URL,
        json=final_json,
        headers=HEADERS,
    )

    hash = response.json()["IpfsHash"]
    json_uri = IPFS_IMAGE_URL.format(hash)

    print(f"You uploaded the JSON file to: {json_uri}")
    print(f"Pinata gateway: {PINATA_IPFS_GATEWAY.format(hash)}\n")

    return json_uri


def local_directory_to_ipfs(directory):
    """Upload a local directory to ipfs using pinata

    Args:
        directory (str): Path to local directory

    Raises:
        Exception: If the local directory does not exists or it's empty

    Returns:
        str: URI of the directory on IPFS
    """
    # Check if exists
    if not os.path.exists(directory):
        raise Exception(f"The directory {directory} does not exist")

    # Check if it's empty
    if len(os.listdir(directory)) == 0:
        raise Exception(f"The directory {directory} is empty")

    # Create the files data for the post request
    files = []
    upload_directory_name = directory.split(os.sep)[-1]
    files.append(
        ("pinataMetadata", (None, '{"name":"' + directory.split(os.sep)[-1] + '"}'))
    )
    for root, dirs, files_ in os.walk(os.path.abspath(directory)):
        for file in files_:
            files.append(
                (
                    "file",
                    (
                        os.path.join(upload_directory_name, file),
                        open(os.path.join(root, file), "rb"),
                    ),
                )
            )

    # Send the request to pinata
    response = requests.post(
        PINATA_PIN_FILE_URL,
        headers=HEADERS,
        files=files,
    )

    hash = response.json()["IpfsHash"]
    file_uri = IPFS_IMAGE_URL.format(hash)

    print(f"You uploaded the file to: {file_uri}")
    print(f"Pinata gateway: {PINATA_IPFS_GATEWAY.format(hash)}")

    return file_uri
