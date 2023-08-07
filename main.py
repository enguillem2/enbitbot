#!/home/guillem/python/test/venv/bin/python
from ethereum import *
from telegram import *
from system import *
from trade import *
if __name__ == "__main__":

    # print(w3_pulse_testnet.is_connected())
   
    # balance=get_balance(address_airdrops,provider=w3_bsc)
    # print("balance of bsc",address_airdrops," is ",balance)

    # balance=get_balance(address_airdrops,provider=w3_goerli)
    # print("balance of goerli",address_airdrops," is ",balance)

    # balance=get_balance(address_airdrops,provider=w3_ethereum)
    # print("balance of ETHEREUM",address_airdrops," is ",balance)

    # balance=get_balance(address_airdrops,provider=w3_zksync)
    # print("balance of zksync",address_airdrops," is ",balance)

    # balance=get_balance(address_airdrops,provider=w3_polygon)
    # print("balance of polygon",address_airdrops," is ",balance)

    # who_address="0xF977814e90dA44bFA03b6295A0616a897441aceC"
    # balance=get_token_balance(usdt_eth,who_address,provider=w3_ethereum)
    # print(f"balance in ethereum {who_address}:{balance}")
    
    # balance=get_token_balance(busdt,who_address,provider=w3_bsc)
    # print(f"balance in bsc {who_address}:{balance}")

    # who_address="0x8Bc9a90b081d23C946c5576D0F96001cEeD61D7f"
    # balance=get_token_balance(usdt_pls,who_address,provider=w3_pulse)
    # print(f"balance in pls {who_address}:{balance}")

    # price = get_pair_price(contract_WPulse,contract_dai_pls)
    # print("price",price)

    # price = get_pair_price(contract_WPulse,contract_dai_pls,router_address=router_pulsev2)
    # print("price router2",price)


    
    # price = get_pair_price(contract_wbtc_pls,contract_dai_pls)
    # print("price",price)
    # price = get_pair_price(contract_wbtc_pls,contract_dai_pls,router_address=router_pulsev2)
    # print("price router2",price)

    #balanc de pdai
    balanc_pdai=int(get_token_balance(contract_pdai,address_brave))
    price=get_pair_price(contract_pdai,contract_plsx,amount=1)
    # print(balanc_pdai,price["price"],balanc_pdai*price["price"])
    cuantitat_inicial=1000000
    loaded_from_file=False
    if balanc_pdai==0:
        balanc_pdai=load_pickle("quantitat_pdai")
        loaded_from_file=True
        print(f"loaded value {balanc_pdai} from disk")
    else:
        save_picke("quantitat_pdai",balanc_pdai)
    final=balanc_pdai*price["price"]
    benefici=final-cuantitat_inicial
    percent=benefici/cuantitat_inicial*100
    max_percent=get_max_percent()
    print(f"max_percent {max_percent} percent {percent}")
    if percent > (max_percent+2):
        send_message(f"la cosa puja {percent}")
        set_max_percent(percent)
    diferencia=max_percent-percent
    if diferencia > 2:
        send_message(f"la cosa baixa <{diferencia}% ")
    print(percent,balanc_pdai,final)
    if percent>10 and not loaded_from_file > 0:
        send_message(f"BENEFICI {percent}")
    if percent < -5 and not loaded_from_file>0:
        send_message(f"PERDUA {percent}")
    if percent < 5 and not loaded_from_file:
        send_message(f"ENTRA {percent}")


    