from brownie import Dogeviathan, accounts, network, config
from brownie import web3


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]

    counter = dogeviathan.tokenCounter()

    for t in range(0, counter):
        print("Counter {}, random number {}, and Void {}".format(
            t, dogeviathan.tokenIdToRand(t), dogeviathan.tokenIdToVoid(t)))