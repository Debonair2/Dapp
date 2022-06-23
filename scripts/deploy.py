import os
from brownie import accounts, USDC, AUSD, DefiBank
from dotenv import load_dotenv
load_dotenv()
from web3 import Web3
def main():
    account = accounts.add("0xe562f36cf0b6004aaab828ced73526b665829df471371328af7b9d23e346d3b1")
    usdc_addr= USDC.deploy({"from": account})
    ausd_addr= AUSD.deploy({"from": account})

    DefiBank.deploy(usdc_addr, ausd_addr, {"from": account})