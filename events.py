# from web3 import Web3
from config import *
from abis import *
import pickle
from ethereum import *
from datetime import datetime
from pulsexread import get_liquidity_2,get_tiker,get_liquidity


import asyncio
import json
from contracts import *

# add your blockchain connection information
infura_url = 'ADDYOURINFURAURL'
web3 = w3_pulse

# uniswap address and abi
# contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)
contract = web3.eth.contract(address=pulse_factory, abi=factory_abi)


# define function to handle events and print to the console
def handle_event(event):
    eve = json.loads(Web3.to_json(event))
    pair = eve["args"]["pair"]
    token0 = eve["args"]["token0"]
    token0_tiker=get_tiker(token0)
    token1 = eve["args"]["token1"]
    token1_tiker=get_tiker(token1)
    # and whatever
    liquidity=get_liquidity_2(pair)
    pair_tiker = f"{token0_tiker}_{token1_tiker}"
    now=datetime.now()
    dt_string=now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"pair: {pair} token0: {token0} token1: {token1} {token0_tiker}_{token1_tiker} {dt_string} liquidity: {liquidity}")


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.PairCreated.create_filter(
        fromBlock='latest')
    # block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
        # log_loop(block_filter, 2),
        # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()
