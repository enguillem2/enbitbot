from config import *
from contracts_bsc import *
from ethereum import *

def send_amount(w3=w3_bsc_testnet):
    account_1 = w3.to_checksum_address(address_airdrops)
    account_2 = w3.to_checksum_address(address_brave)
    nonce = w3_pulse.eth.get_transaction_count(account_1)

    print("nonce",nonce)
     #build the transaction
    # Variables
    chain_id = 97
    gas = 300000
    gas_price= 100000000000
    value =0.01
    tx_build={
        'chainId': chain_id,
        'gas':gas,
        'gasPrice':gas_price,
        'nonce':nonce,
        'value':value,
        'to':account_2
    }
    print(tx_build)

    # Sign transaction
    tx_signed = w3.eth.account.sign_transaction(tx_build, pk_mainnet)
    print(tx_signed)

    # Send transaction
    sent_tx = w3.eth.send_raw_transaction(tx_signed.rawTransaction)
    print(w3.to_hex(sent_tx))

if __name__ == "__main__":
    # balance=get_balance(address_airdrops,w3_bsc_testnet)
    # print(address_airdrops,balance)
    # send_amount()
    test=get_pair_price(address_btcb,address_dai_bsc,w3_bsc,router_bsc)
    print(f"test {test}")
    test=get_pair_price(address_cake,address_dai_bsc,w3_bsc,router_bsc,amount=10)
    print(f"test {test}")



