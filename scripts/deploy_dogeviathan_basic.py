#!/usr/bin/python3
from brownie import DogeviathanBasic, accounts, network, config

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    dogeviathan_basic = DogeviathanBasic.deploy(
        {"from": accounts[0]},
        publish_source=True
    )
    return dogeviathan_basic
