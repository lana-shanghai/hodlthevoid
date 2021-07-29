#!/usr/bin/python3
import os
import requests
import json
from brownie import Dogeviathan, network, accounts, config
from metadata import sample_metadata
from pathlib import Path
from dotenv import load_dotenv

PINATA_BASE_URL = 'https://api.pinata.cloud/'
endpoint = 'pinning/pinFileToIPFS'

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
            "name": "AO XIV 13 # " + str(token_id),
            "description": "A Hodl The Void NFT",
            "image": "https://gateway.pinata.cloud/ipfs/QmcKbMCBVxge8daFUsXT37BHyDY7r8Vq8GBNXYGGxhteVD?filename=umbrella.JPG",
            "attributes": [
                {"display_type": "number", "trait_type": "mobility", "value": t[0], "max_value": 5}, 
                {"display_type": "number", "trait_type": "energy", "value": t[1], "max_value": 5}, 
                {"display_type": "number", "trait_type": "oxygen", "value": t[2], "max_value": 5}, 
                {"display_type": "number", "trait_type": "codex", "value": t[3], "max_value": 5}, 
                {"display_type": "number", "trait_type": "justice", "value": t[4], "max_value": 5}]
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
            image_to_upload = image_uri
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w+") as file:
                json.dump(collectible_metadata, file)

        try:
            if not dogeviathan.tokenURI(token_id).startswith("https://"):
                print("Setting tokenURI of {}".format(token_id))
                token_uri = upload_to_pinata(metadata_file_name)
                if Path(metadata_file_name).exists():
                    set_tokenURI(token_id, dogeviathan,
                            token_uri)
            else:
                print("Skipping {}, we already set that tokenURI!".format(token_id))
        except ValueError:
            print("Non-existent token")

def upload_to_pinata(file):
    filename = file.split('/')[-1:][0]
    headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
            'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}


    with open (file) as metadata_file:
        response = requests.post(PINATA_BASE_URL + endpoint,
                                files={"file": (filename, metadata_file)},
                                headers=headers)
        print(response.json())
        print('https://gateway.pinata.cloud/ipfs/{}'.format(response.json()['IpfsHash']))
    return 'https://gateway.pinata.cloud/ipfs/{}'.format(response.json()['IpfsHash'])

def set_tokenURI(token_id, dogeviathan, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    attacker = accounts.add(config["wallets"]["from_attacker_key"])
    dogeviathan.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {} id {}".format(dogeviathan.address, token_id)
        )

    print('Please give up to 20 minutes, and hit the "refresh metadata" button')