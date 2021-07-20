#!/usr/bin/python3
from brownie import web3
from brownie import Dogeviathan, accounts, config
from scripts.helpful_scripts import fund_with_link
import time
from metadata import sample_metadata

# contract_address = web3.toChecksumAddress(0xa7F8C00459E23bb618C11e847e9eBd6238883c49)

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]

    fund_with_link(dogeviathan.address)

    amount = dogeviathan.getVoidPrice()
    transaction = dogeviathan.createCollectible("None", {"from": dev, "value": amount})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    time.sleep(35)
    requestId = transaction.events["requestedCollectible"]["requestId"]
    print("requestId", requestId)
    
    counter = dogeviathan.tokenCounter()
    print("Counter {}".format(counter))
    
    for t in range(0, counter):
        real_rand = dogeviathan.tokenIdToRand(t)
        print("Counter: {}".format(t), real_rand)
        dogeviathan.randToVoid(real_rand, {"from": dev})
        print("Void {}".format(dogeviathan.tokenIdToVoid(t)))

