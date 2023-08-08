"""Manual transfer script.

- For a hardcoded token, asks to address and amount where to transfer tokens.

- Waits for the transaction to complete
"""
import datetime
import os
import sys
from decimal import Decimal

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import HTTPProvider, Web3
from web3.middleware import construct_sign_and_send_raw_middleware

from eth_defi.abi import get_deployed_contract
from eth_defi.token import fetch_erc20_details
# from eth_defi.txmonitor import wait_transactions_to_complete

from config import *
from contracts import *

print (address_airdrops)
ERC_20_TOKEN_ADDRESS=contract_plsx

web3 = w3_pulse
print(f"Connected to blockchain, chain id is {web3.eth.chain_id}. the latest block is {web3.eth.block_number:,}")

# Read and setup a local private key
private_key = "0x"+pk_mainnet
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
account: LocalAccount = Account.from_key(private_key)
web3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

# Show users the current status of token and his address
erc_20 = get_deployed_contract(web3, "ERC20MockDecimals.json", ERC_20_TOKEN_ADDRESS)
token_details = fetch_erc20_details(web3, ERC_20_TOKEN_ADDRESS)

print(f"Token details are {token_details}")

balance = erc_20.functions.balanceOf(account.address).call()
eth_balance = web3.eth.getBalance(account.address)

print(f"Your balance is: {token_details.convert_to_decimals(balance)} {token_details.symbol}")
print(f"Your have {eth_balance/(10**18)} ETH for gas fees")

# Ask for transfer details
decimal_amount = input("How many tokens to transfer? ")
to_address = address_brave

# Some input validation
try:
    decimal_amount = Decimal(decimal_amount)
except ValueError as e:
    raise AssertionError(f"Not a good decimal amount: {decimal_amount}") from e

assert web3.isChecksumAddress(to_address), f"Not a valid address: {to_address}"

# Fat-fingering check
print(f"Confirm transferring {decimal_amount} {token_details.symbol} to {to_address}")
confirm = input("Ok [y/n]?")

if not confirm.lower().startswith("y"):
    print("Aborted")
    sys.exit(1)

# Convert a human-readable number to fixed decimal with 18 decimal places
raw_amount = token_details.convert_to_raw(decimal_amount)
tx_hash = erc_20.functions.transfer(to_address, raw_amount).transact({"from": account.address})

# This will raise an exception if we do not confirm within the timeout
print(f"Broadcasted transaction {tx_hash.hex()}, now waiting 5 minutes for mining")

