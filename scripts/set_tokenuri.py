#!/usr/bin/python3
from brownie import Dogeviathan, accounts, network, config
from pathlib import Path



def main():
    print("Working on " + network.show_active())
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]
    number_of_voids = dogeviathan.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_voids)
    )
    for token_id in range(1,number_of_voids):
        if not dogeviathan.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            + ".json"
            )
            if Path(metadata_file_name).exists():
                set_tokenURI(token_id, dogeviathan,
                         "https://gateway.pinata.cloud/ipfs/QmeBhu8dcrCLdaVFd6KNyQ8oYnTyUb2MWPBuYJrt3UopRb")
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    attacker = accounts.add(config["wallets"]["from_attacker_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {} id {}".format(nft_contract.address, token_id)
        )

    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
