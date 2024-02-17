import glob
import os
import argparse
import json

from config import *
from abis import *
import pickle
from ethereum import *
from datetime import datetime
 
web3 = w3_pulse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--network",dest="network",help="Network to connect")
    options = parser.parse_args()

    if not options.network:
        parser.error("[-] Please especify a networ, use --help for info")

    return options

def depth_pulse(file):
    print(f"reading surface information file: {file}")
    # Opening JSON file
    f = open(file)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    for t in data:
        pair1ContractAdress=t["poolContract1"]
        pair2ContractAdress=t["poolContract2"]
        pair3ContractAdress=t["poolContract3"]

        trade1Direction=t["poolDirectionTrade1"]
        trade2Direction=t["poolDirectionTrade2"]
        trade3Direction=t["poolDirectionTrade3"]

        swap1=t["swap1"]
        swap2=t["swap2"]
        swap3=t["swap3"]

        tradeDesc1=t["tradeDesc1"]
        tradeDesc2=t["tradeDesc2"]
        tradeDesc3=t["tradeDesc3"]


        acquiredCoinT1=getPricePulse(pair1ContractAdress,amountIn=1,tradeDirection=trade1Direction)
        acquiredCoinT2=getPricePulse(pair2ContractAdress,acquiredCoinT1,tradeDirection=trade2Direction)
        acquiredCoinT3=getPricePulse(pair3ContractAdress,acquiredCoinT2,tradeDirection=trade3Direction)
        if (float(acquiredCoinT3)>float(1)):
            print(f"1 {acquiredCoinT3}")
            print(f"{tradeDesc1} {tradeDesc2} {tradeDesc3}")


    # Closing file
    f.close()

def getPricePulse(pair1ContractAdress,amountIn=1,tradeDirection="baseToQuote"):
    address=web3.to_checksum_address(pair1ContractAdress)
    pairContract = web3.eth.contract(address=address, abi=pairs_abi)
    token0=pairContract.functions.token0().call()
    token1=pairContract.functions.token1().call()
    addressArray=[token0,token1]
    tokenInfoArray=[]
    i=0
    for adr in addressArray:
        tokenContract=web3.eth.contract(address=adr,abi=erc20_abi)
        decimals = tokenContract.functions.decimals().call()
        name = tokenContract.functions.name().call()
        token1_tiker = tokenContract.functions.symbol().call()
        obj={}
        obj={"id":f"token{i}","tokenAddress":adr,"tokenSymbol":token1_tiker,"tokenName":name,"tokenDecimals":decimals}

        tokenInfoArray.append(obj)

        i+=1
    #identify the correct as A and B
    inputTokenA=''
    inputDecimalsA=0
    inputTokenB=''
    inputDecimalsB=0
    factorA=0
    factorB=0

    if tradeDirection=="baseToQuote":
        inputTokenA=tokenInfoArray[0]["tokenAddress"]
        inputDecimalsA=tokenInfoArray[0]["tokenDecimals"]
        symbolA=tokenInfoArray[0]["tokenSymbol"]
        
        inputTokenB=tokenInfoArray[1]["tokenAddress"]
        inputDecimalsB=tokenInfoArray[1]["tokenDecimals"]
        symbolB=tokenInfoArray[1]["tokenSymbol"]

    if tradeDirection == "quoteToBase":
        inputTokenA=tokenInfoArray[1]["tokenAddress"]
        inputDecimalsA=tokenInfoArray[1]["tokenDecimals"]
        symbolA=tokenInfoArray[1]["tokenSymbol"]

        
        inputTokenB=tokenInfoArray[0]["tokenAddress"]
        inputDecimalsB=tokenInfoArray[0]["tokenDecimals"]
        symbolB=tokenInfoArray[0]["tokenSymbol"]
    factorA=10**inputDecimalsA
    factorB=10**inputDecimalsB

    price = get_pair_price(inputTokenA,inputTokenB,amount=amountIn)
    pr=0
    if price!=0:
        pr=price['price']
    return pr
        





def depth_ethereum(file):
    print(f"file: {file}")



if __name__ == "__main__":
    options=get_arguments()
    network=options.network

    if network=="pulsechain":
        list_of_files = glob.glob('json/pulse/*') # * means all if need specific format then *.csv
        depth_pulse(max(list_of_files, key=os.path.getctime))

    elif network=="ethereum":
        list_of_files = glob.glob('json/ethereum/*') # * means all if need specific format then *.csv
        depth_pulse(max(list_of_files, key=os.path.getctime))

