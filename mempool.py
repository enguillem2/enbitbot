
# from web3 import Web3
from config import *
import asyncio
import json
from contracts import *

import asyncio
import json
web3=w3_pulse
router = web3.to_checksum_address(router_address_pulse)
routerv2 = web3.to_checksum_address(router_pulsev2)


def handle_event(event):
    # print the transaction hash
    # print(Web3.toJSON(event))

    # use a try / except to have the program continue if there is a bad transaction in the list
    try:
        # remove the quotes in the transaction hash
        transaction = Web3.to_json(event).strip('"')
        # use the transaction hash that we removed the '"' from to get the details of the transaction
        transaction = web3.eth.get_transaction(transaction)
        # print the transaction and its details
        to=transaction['to']
        # print(to)
        if to == router:
            print("v1",to)
        if to == router_v2:
            print("v2",to)

    except Exception as err:
        # print transactions with errors. Expect to see transactions people submitted with errors 
        pass
        # print(f'error: {err}')


async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

if __name__ == "__main__":
    print(web3.is_connected())

    tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(tx_filter, 2)))
    finally:
        loop.close()

