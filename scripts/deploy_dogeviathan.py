#!/usr/bin/python3
from brownie import Dogeviathan, accounts, network, config

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    dogeviathan = Dogeviathan.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": accounts[0]},
        publish_source=True
    )
    return dogeviathan
