#!/usr/bin/python3
from brownie import Dogeviathan
from scripts.helpful_scripts import fund_with_link


def main():
    dogeviathan = Dogeviathan[len(Dogeviathan) - 1]
    fund_with_link(dogeviathan.address)