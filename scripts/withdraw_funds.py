from brownie import Dogeviathan, accounts, config

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]

    dogeviathan.withdraw({"from": dev})