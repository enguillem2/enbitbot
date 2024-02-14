# from web3 import Web3
from config import *
from abis import *
import pickle
from ethereum import *
from datetime import datetime


import asyncio
import json
from contracts import *

# web3=w3_ethereum
web3 = w3_pulse

# factory_abi=json.load(factory_abi)
factory_address = pulse_factory
# factory_address=uniswap_factory
factory_contract = web3.eth.contract(address=factory_address, abi=factory_abi)


def are_new_pairs():
    old_pairs = pickle.load(open("all_pairs.pkl", "rb"))
    only_address = pickle.load(open("only_address.pkl", "rb"))
    allPairsLength = factory_contract.functions.allPairsLength().call()
    new_pairs=[]
    print(len(old_pairs), len(only_address), allPairsLength)
    for i in range(1, allPairsLength):
        allPairs_address = factory_contract.functions.allPairs(i).call()
        if allPairs_address not in only_address:
            new_pair = get_pair(allPairs_address)
            only_address.append(allPairs_address)
            old_pairs.append(new_pair)
            print(i, "new pair", new_pair["pairs"])
            new_pairs.append(new_pairs)
    with open("all_pairs.pkl", "wb") as f:
        pickle.dump(old_pairs, f)
    with open("only_address.pkl", "wb") as f:
        pickle.dump(only_address, f)
    with open("new_pairs.pkl","wb") as f:
        pickle.dump(new_pairs)


def get_pair(address):
    contract = web3.eth.contract(address=address, abi=pairs_abi)
    supply = contract.functions.totalSupply().call()

    token0 = contract.functions.token0().call()
    token0_contract = web3.eth.contract(address=token0, abi=erc20_abi)
    try:
        token0_tiker = token0_contract.functions.symbol().call()
    except:
        token0_tiker = "NONE"

    token1 = contract.functions.token1().call()
    token1_contract = web3.eth.contract(address=token1, abi=erc20_abi)
    try:
        token1_tiker = token1_contract.functions.symbol().call()
    except:
        token1_tiker = "NONE"
    pair_tiker = f"{token0_tiker}_{token1_tiker}"
    now=datetime.now()
    dt_string=now.strftime("%Y-%m-%d $H:%M:%S")
    pair = {
        "contract": address,
        "supply": supply,
        "pairs": pair_tiker,
        "datetime":dt_string
    }
    return pair


def get_tiker(token):
    token_contract = web3.eth.contract(address=token, abi=erc20_abi)
    token1_tiker=""
    try:
        token1_tiker = token_contract.functions.symbol().call()
    except:
        token1_tiker = "NONE"
    return token1_tiker

def get_all_pairs():
    allPairsLength = factory_contract.functions.allPairsLength().call()
    print(allPairsLength)
    all_pairs = []
    only_address = []

    for i in range(0, allPairsLength):
        allPairs_address = factory_contract.functions.allPairs(i).call()
        print("allPairs", allPairs_address)
        contract = web3.eth.contract(address=allPairs_address, abi=pairs_abi)
        symbol = contract.functions.name().call()
        supply = contract.functions.totalSupply().call()

        token0 = contract.functions.token0().call()
        token0_contract = web3.eth.contract(address=token0, abi=erc20_abi)
        try:
            token0_tiker = token0_contract.functions.symbol().call()
        except:
            token0_tiker = "NONE"

        token1 = contract.functions.token1().call()
        token1_contract = web3.eth.contract(address=token1, abi=erc20_abi)
        try:
            token1_tiker = token1_contract.functions.symbol().call()
        except:
            token1_tiker = "NONE"

        pair = f"{token0_tiker}_{token1_tiker}"

        print(i, allPairs_address, supply, pair)
        now=datetime.now()
        dt_string=now.strftime("%Y-%m-%d $H:%M:%S")
        pair = {
            "contract": allPairs_address,
            "supply": supply,
            "pairs": pair,
            "datetime":dt_string
        }
        all_pairs.append(pair)
        only_address.append(allPairs_address)
        with open("all_pairs.pkl", "wb") as f:
            pickle.dump(all_pairs, f)
        with open("only_address.pkl", "wb") as f:
            pickle.dump(only_address, f)

def get_reserves():
    old_pairs = pickle.load(open("all_pairs.pkl", "rb"))
    only_address = pickle.load(open("only_address.pkl", "rb"))
    for i in range(1, 3):
        print(f"addres:: {only_address[i]}")
        get_liquidity(old_pairs[i])

def get_liquidity_2(pair):
    pair_address=pair
    pair_contract = web3.eth.contract(address=pair_address, abi=pairs_abi)
    reserves=pair_contract.functions.getReserves().call()

    token0=pair_contract.functions.token0().call()
    token0_tiker=get_tiker(token0)
    decimals0=get_decimals(token0)
    factor0=10**decimals0


    token1=pair_contract.functions.token1().call()
    token1_tiker=get_tiker(token1)
    decimals1=get_decimals(token1)
    factor1=10**decimals1
    liquid=0


    price0=get_pair_price(token0,dai_ethereum)
    # price0=price0["price"]
    price1=get_pair_price(token1,dai_ethereum)

    if price0!=0:
        res0=reserves[0]/factor0
        p0=price0["price"]
        liq0=res0*p0
        liquid=liq0*2

    if price1!=0:
        res1=reserves[1]/factor1
        p1=price1["price"]
        liq1=res1*p1
        liquid=liq1*2
    
    return liquid

    
    
    
    # price1=get_pair_price(token1,dai_ethereum)
    # print(f"price1 {price1}")
    # if price1!=0:
    #     price1=price1["price"]
    # else:
    #     if price0!=0:
    #         ##cercam l'equivalencia
    #         print("canvi preu")
    #         preu_equivalent=get_pair_price(token1,token0)
    #         price1=preu_equivalent["price"]*price0
    # print(f"price0 {price0} price1 {price1}")


def get_liquidity(pair):
    pair_address=pair["contract"]
    pair_contract = web3.eth.contract(address=pair_address, abi=pairs_abi)
    reserves=pair_contract.functions.getReserves().call()

    token0=pair_contract.functions.token0().call()
    token1=pair_contract.functions.token1().call()
    print(f"{pair['pairs']} token0 {token0} token1 {token1}")

    price0=get_pair_price(token0,dai_ethereum)
    price0=price0["price"]
    print(f"price0 {price0}")
    
    
    
    price1=get_pair_price(token1,dai_ethereum)
    print(f"price1 {price1}")
    if price1!=0:
        price1=price1["price"]
    else:
        if price0!=0:
            ##cercam l'equivalencia
            print("canvi preu")
            preu_equivalent=get_pair_price(token1,token0)
            price1=preu_equivalent["price"]*price0
    print(f"price0 {price0} price1 {price1}")

    # price1=get_pair_price(token1,dai_ethereum,provider=web3)
    

    total_liquidity=0

    total_liquidity=reserves[0]*price0+reserves[1]*price1

    print(f"reserves: {reserves} total liquidity: {total_liquidity}")



if __name__ == "__main__":
    get_all_pairs()
    # get_liquidity_2("0xDe6F2299b9791b7F4FE7f2edCF4cFA17fadf4CEC")
    #are_new_pairs()
    # get_reserves()

