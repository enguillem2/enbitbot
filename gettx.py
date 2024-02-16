# import dependencies
from config import *
from ethereum import *

from contracts import *
import pickle
from web3 import Web3, HTTPProvider

# # instantiate a web3 remote provider
# # w3 = Web3(HTTPProvider('YOUR_QUICKNODE_HTTP_ENDPOINT'))
# w3 = w3_ethereum
w3 = w3_pulse

# # request the latest block number
# ending_blocknumber = w3.eth.block_number

# # latest block number minus 100 blocks
# starting_blocknumber = ending_blocknumber - 100

# # filter through blocks and look for transactions involving this address
# blockchain_address = "0x1715a3E4A142d8b698131108995174F37aEBA10D"



# create an empty dictionary we will add transaction data to
tx_dictionary = {}

def getTransactions(start, end, address):
    '''This function takes three inputs, a starting block number, ending block number
    and an Ethereum address. The function loops over the transactions in each block and
    checks if the address in the to field matches the one we set in the blockchain_address.
    Additionally, it will write the found transactions to a pickle file for quickly serializing and de-serializing
    a Python object.'''
    print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}...")
    for x in range(start, end):
        block = w3.eth.get_block(x, True)
        for transaction in block.transactions:
            if transaction['to'] == address or transaction['from'] == address:
                with open("transactions.pkl", "wb") as f:
                    hashStr = transaction['hash'].hex()
                    tx_dictionary[hashStr] = transaction
                    pickle.dump(tx_dictionary, f)
                f.close()
    print(f"Finished searching blocks {start} through {end} and found {len(tx_dictionary)} transactions")
    
def get_bridge_value(list_tokens):
    result=[]
    for token in list_tokens:
        print(f"token {token}")
        token_result={}
        balance=get_token_balance(token["contract"], bridge_pulsechain,provider=w3_ethereum)
        price=1
        if token["have_to_get_value"]==1 and token["have_to_invert_value"]==0:
            pair_price=get_pair_price(token["contract"],dai_ethereum,provider=w3_ethereum,router_address=router_v2,amount=1)
            print("pair_price",pair_price,token["contract"])
            price=pair_price["price"]
        if token["have_to_get_value"]==1 and token["have_to_invert_value"]==1:
            price_inverted=get_pair_price(dai_ethereum,token["contract"],provider=w3_ethereum,router_address=router_v2,amount=1)
            price=1/price_inverted["price"]
            print(token["contract"])
            print(f"price_inverted {price_inverted} price {price}")
            # value_btc=bal_wbtc * price_wbtc
            
        value_token=balance*price
        token_result["tiker"]=token["tiker"]
        token_result["balance"]=balance
        token_result["price"]=price
        token_result["value"]=value_token
        result.append(token_result)

    return result




if __name__ == "__main__":
    #getTransactions(starting_blocknumber, ending_blocknumber, blockchain_address)
    total=0

    tokens=get_bridge_value(tokens_bridge)
    for token in tokens:
        print(f'{token["tiker"]}: {token["value"]:,.2f}')
        total+=token["value"]
    print(f"TOTAL: {total:,.2f}")
    



