# import dependencies
from config import *
from ethereum import *

from contracts import *
import pickle
from web3 import Web3, HTTPProvider

# # instantiate a web3 remote provider
# # w3 = Web3(HTTPProvider('YOUR_QUICKNODE_HTTP_ENDPOINT'))
# w3 = w3_ethereum

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
    


if __name__ == "__main__":
    #getTransactions(starting_blocknumber, ending_blocknumber, blockchain_address)
    total=0

    #dai in bridge
    bal_dai=get_token_balance(dai_ethereum, bridge_pulsechain,provider=w3_ethereum)
    total+=bal_dai

    #hex in bridge
    bal_hex = get_token_balance(contract_hex,bridge_pulsechain,provider=w3_ethereum)
    price_hex=get_pair_price(contract_hex,dai_ethereum,provider=w3_ethereum,router_address=router_v2,amount=1)
    value_hex = bal_hex * price_hex["price"]
    total+=value_hex

    #usdc in bridge
    bal_usdc=get_token_balance(contract_pUSDC,bridge_pulsechain,provider=w3_ethereum)
    total+=bal_usdc

    #weth in bridge
    bal_weth=get_token_balance(weth_ethereum,bridge_pulsechain,provider=w3_ethereum)
    price_weth=get_pair_price(weth_ethereum,dai_ethereum,provider=w3_ethereum,router_address=router_v2,amount=1)
    price_weth=get_pair_price(weth_ethereum,dai_ethereum,provider=w3_ethereum,router_address=router_v2,amount=1)

    value_weth=bal_weth*price_weth["price"]
    total+=value_weth

    #wbtc in bridge
    bal_wbtc=get_token_balance(contract_wbtc_eth,bridge_pulsechain,provider=w3_ethereum)
    price_wbtc=get_pair_price(contract_wbtc_eth,dai_ethereum,provider=w3_ethereum,router_address=router_v2,amount=1)
    price_dai_wbtc=get_pair_price(dai_ethereum,contract_wbtc_eth,provider=w3_ethereum,router_address=router_v2,amount=1)
    price_wbtc=1/price_dai_wbtc["price"]
    value_btc=bal_wbtc * price_wbtc
    total+=value_btc


    #usdt in bridge
    bal_usdt=get_token_balance(usdt_eth,bridge_pulsechain,provider=w3_ethereum)

    print(f"balance dai: {bal_dai:,.2f}")
    print(f"balance hex {bal_hex:,.2f} value: {value_hex:,.2f}")
    print(f"balance usdc: {bal_usdc:,.2f}")

    print(f"balance hex {bal_weth:,.2f} value: {value_weth:,.2f}")
    print(f"balance usdt: {bal_usdt:,.2f}")

    print(f"balance wbtc {bal_wbtc:,.2f} value: {value_btc:,.2f}")

    total=bal_dai+value_hex+bal_usdc+value_weth+bal_usdt+value_btc
    print(f"TOTAL: {total:,.2f}")



