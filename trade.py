from system import *
from telegram import *
from ethereum import *

def set_max_percent2(value,cadena):
    file_name=f"percent_{cadena}"
    save_picke(file_name,value)

def set_max_percent(value,tiker_from,tiker_to):
    file_name=f"percent_{tiker_from}_{tiker_to}"
    print(f"seting MAXPERCENT!! {value} {file_name}")
    save_picke(file_name,value)

def get_max_percent(tiker_from,tiker_to):
    value=0
    file_name=f"percent_{tiker_from}_{tiker_to}"
    if is_pickle(file_name):
        value=load_pickle(file_name)
    return value


def getAdressFromTiker(tiker):
    for token in tokens_trade_pls:
        if token["tiker"]==tiker:
            return token["address"]

def calculate_trade(tiker_from,tiker_to):
    print(tiker_from,tiker_to)
    msg=f"{tiker_from}_{tiker_to}\n"
    address_from=getAdressFromTiker(tiker_from)
    address_to=getAdressFromTiker(tiker_to)
    print(f"address_from {address_from} address_to {address_to}")
    #balanc de from
    balance_from=int(get_token_balance(address_from,address_brave))
    price=get_pair_price(address_from,address_to,amount=1)
    # print(balance_from,price["price"],balance_from*price["price"])
    cuantitat_inicial=1000000
    loaded_from_file=False
    if balance_from==0:
        balance_from=load_pickle(f"quantitat_{tiker_from}_{tiker_to}")
        loaded_from_file=True
        print(f"loaded value {balance_from} from disk")
    else:
        save_picke(f"quantitat_{tiker_from}_{tiker_to}",balance_from)
    final=balance_from*price["price"]
    benefici=final-cuantitat_inicial
    percent=benefici/cuantitat_inicial*100
    max_percent=get_max_percent(tiker_from,tiker_to)
    print(f"max_percent {max_percent} percent {percent}")
    if percent > (max_percent+2):
        msg+=f"la cosa puja {percent}"
        send_message(msg)
        set_max_percent(percent,tiker_from,tiker_to)
    diferencia=max_percent-percent
    if diferencia > 2:
        msg+=f"la cosa baixa {percent}"
        send_message(msg)
    print(percent,balance_from,final)
    if percent>10 and not loaded_from_file > 0:
        msg+=f"BENEFICI {percent}"
        send_message(msg)
    # if percent < -3 and not loaded_from_file>0:
    #     msg+=f"PERDUA {percent}"
    #     send_message(msg)
    if percent > -7 and percent < 5 and not loaded_from_file:
        msg+=f"RANG BAIX {percent}"
        send_message(msg)




if __name__ == "__main__":
    print("trade")