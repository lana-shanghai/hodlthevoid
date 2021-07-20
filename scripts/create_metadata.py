#!/usr/bin/python3
import os
import requests
import json
from brownie import Dogeviathan, network
from metadata import sample_metadata
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

image_uri = "https://gateway.pinata.cloud/ipfs/QmcKbMCBVxge8daFUsXT37BHyDY7r8Vq8GBNXYGGxhteVD?filename=umbrella.JPG"


def main():
    print("Working on " + network.show_active())
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]
    number_of_voids = dogeviathan.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_voids)
    )
    write_metadata(number_of_voids, dogeviathan)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] = "name"
            collectible_metadata["description"] = "A Hodl The Void NFT".format(
                collectible_metadata["name"]
            )
            image_to_upload = image_uri
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add

'''
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri
'''