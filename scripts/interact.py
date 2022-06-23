import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv


def main():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    usdc_contract = Contract("0x96845257d64776b53b3D4A0973b2c86C0d3F8D6c")
    defi_contract = Contract("0xF0a01255e33b1fB7923ad7425a3E3378024A09E9")

    print(f" Before function call current usdc token balance is {defi_contract.depositBalance(account)}")
    usdc_contract.approve(defi_contract, 10000, {"from": account})
    defi_contract.depositToken(10000,{"from": account})

    print(f" After function call current usdc token balance is {defi_contract.depositBalance(account)}")

    defi_contract.withdraw(100,{"from": account})

    print(f" Current balance after withdrawing usdc token deposit balance is {defi_contract.depositBalance(account)}")
