# from web3 import Web3
from config import *
from abis import *

import asyncio
import json
from contracts import *

# web3=w3_ethereum
web3=w3_pulse

#factory_abi=json.load(factory_abi)
factory_address=pulse_factory
factory_contract=web3.eth.contract(address=factory_address,abi=factory_abi)

allPairsLength = factory_contract.functions.allPairsLength().call()
print(allPairsLength)

for i in range(1, allPairsLength):
    allPairs_address = factory_contract.functions.allPairs(i).call()
    # print("allPairs",allPairs_address)
    contract = web3.eth.contract(address=allPairs_address, abi=pairs_abi)
    symbol = contract.functions.name().call()
    supply = contract.functions.totalSupply().call()
    print(allPairs_address, symbol,supply)