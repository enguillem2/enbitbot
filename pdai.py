from config import *
from abis import *


dssPsm="0x89B78CfA322F6C5dE0aBcEecab66Aee45393cC5A"
elContracte = w3_pulse.eth.contract(address=dssPsm,abi=dssPsmABI)

def convert(num):
    # Variables

    account_1 = address_airdrops
    nonce = w3_pulse.eth.get_transaction_count(account_1)

    chain_id = 369
    gas = 3000000
    gas_price= 1000000000000
    value =num

    # Caim Winnings
    tx_build = elContracte.functions.sellGem(account_1,value).build_transaction({
        "chainId": chain_id,
        "gas": gas,
        "gasPrice": gas_price,
        "nonce": nonce
    })
    print(tx_build)

    # Sign transaction
    tx_signed = w3_pulse.eth.account.sign_transaction(tx_build, pk_mainnet)
    print(tx_signed)

    # Send transaction
    sent_tx = w3_pulse.eth.send_raw_transaction(tx_signed.rawTransaction)
    print("tx_hash",w3_pulse.to_hex(sent_tx))

if __name__ == "__main__":
    convert(10)
