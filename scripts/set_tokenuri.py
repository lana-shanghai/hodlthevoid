#!/usr/bin/python3
from brownie import Dogeviathan, accounts, network, config
from metadata import sample_metadata



def main():
    print("Working on " + network.show_active())
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]
    number_of_voids = dogeviathan.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_voids)
    )
    for token_id in range(number_of_voids):
        if not dogeviathan.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, dogeviathan,
                         "https://gateway.pinata.cloud/ipfs/QmTobGXfo7Rymx1mWfA11aXgVEVg2M2gN8gqEwownmL2P8")
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {} id {}".format(nft_contract.address, token_id)
        )

    print('Please give up to 20 minutes, and hit the "refresh metadata" button')


