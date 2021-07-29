#!/usr/bin/python3
from brownie import Dogeviathan, accounts, network, config

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False # Currently having an issue with this
    dogeviathan = Dogeviathan.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": accounts[0]},
        publish_source=True
    )
    return dogeviathan
