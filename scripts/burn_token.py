from brownie import Dogeviathan, accounts, config

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    attacker = accounts.add(config["wallets"]["from_attacker_key"])
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]

    dogeviathan.burn(0, {"from": dev})
    #dogeviathan.burn(1, {"from": attacker})