import os
from pathlib import Path
import requests
from scripts.helpful_scripts import IPFS_IMAGE_URL
import os


PINATA_PIN_FILE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def upload_to_pinata(directory):
    if not os.path.exists(directory):
        raise Exception(f"The directory {directory} does not exist")

    headers = {
        "pinata_api_key": os.environ["PINATA_API_KEY"],
        "pinata_secret_api_key": os.environ["PINATA_SECRET_API_KEY"],
    }

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

    response = requests.post(
        PINATA_PIN_FILE_URL,
        headers=headers,
        files=files,
    )

    hash = response.json()["IpfsHash"]
    file_uri = IPFS_IMAGE_URL.format(hash)

    print(f"You uploaded the file to: {file_uri}")

    return file_uri


def main():
    directory = "/Users/alex/Work/Personal/jesi-ntf-market/hexagonitos"
    upload_to_pinata(directory)
