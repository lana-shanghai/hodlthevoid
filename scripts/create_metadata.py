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


def write_metadata(token_ids, dogeviathan):
    for token_id in range(token_ids):
        t = dogeviathan.tokenIdToVoid(token_id)
        collectible_metadata = {
            "name": "Void",
            "description": "NFT",
            "image": "https://gateway.pinata.cloud/ipfs/QmcKbMCBVxge8daFUsXT37BHyDY7r8Vq8GBNXYGGxhteVD?filename=umbrella.JPG",
            "attributes": [
                {"trait_type": "mobility", "value": t[0], "max_value": 5}, 
                {"trait_type": "energy", "value": t[1], "max_value": 5}, 
                {"trait_type": "oxygen", "value": t[2], "max_value": 5}, 
                {"trait_type": "codex", "value": t[3], "max_value": 5}, 
                {"trait_type": "justice", "value": t[4], "max_value": 5}]
        }
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
            tokenID = dogeviathan.tokenCounter()
            collectible_metadata["name"] = "AO XIV 13 # " + str(tokenID)
            collectible_metadata["description"] = "A Hodl The Void NFT"
            image_to_upload = image_uri
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w+") as file:
                json.dump(collectible_metadata, file)
