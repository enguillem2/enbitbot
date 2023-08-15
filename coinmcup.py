from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint 
import os

import csv

from config import key_cmc

pp = pprint.PrettyPrinter(indent=4)

symbolstr=','.join(('BTC,ETH,BNB,XRP,USDT,ADA,DOT,UNI,LTC,LINK,XLM,BCH', 
        'THETA,FIL,USDC,TRX,DOGE,WBTC,VET,SOL,KLAY,EOS,XMR,LUNA', 
        'MIOTA,BTT,CRO,BUSD,FTT,AAVE,BSV,XTZ,ATOM,NEO,AVAX,ALGO', 
        'CAKE,HT,EGLD,XEM,KSM,BTCB,DAI,HOT,CHZ,DASH,HBAR,RUNE,MKR,ZEC',
        'ENJ,DCR,MKR,ETC,GRT,COMP,STX,NEAR,SNX,ZIL,BAT,LEO,SUSHI', 
        'MATIC,BTG,NEXO,TFUEL,ZRX,UST,CEL,MANA,YFI,UMA,WAVES,RVN',
        'ONT,ICX,QTUM,ONE,KCS,OMG,FLOW,OKB,BNT,HNT,SC,DGB,RSR,DENT',
        'ANKR,REV,NPXS,VGX,FTM,CHSB,REN,IOST,BTMX,CELO,PAX,CFX,HEX,PLS,PLSX,DAI,USDT,USDC'))
# Makes symbolstr into a list for later for loop
symbol_list=symbolstr.split(',')
url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

headers = {
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': key_cmc,
}
parameters = {
'id':'1,2,3,4'
}

def call_url(url,id):
    print(url)
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': key_cmc,
    }
    parameters = {
    'id':id
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
        # pp.pprint(data)
        

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        data = json.loads(response.text)
        pp.pprint(data)

def test():
    print("test",key_cmc)
    print(url)

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        pp.pprint(data)
        

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        data = json.loads(response.text)
        pp.pprint(data)

def test2():
    print(url)
    parameters ={
        'symbol':symbolstr
    }
    print(parameters)
    session = Session()
    session.headers.update(headers)
    print(session)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        data = json.loads(response.text)

    
    # pp.pprint(data)
    file_to_open='coinmap.txt'
    line_list=[]
    with open(file_to_open, 'w') as this_csv_file:
        for symbol in symbol_list:
            try:
                thename=data['data'][symbol]['name']
                cid=data['data'][symbol]['id']
                # print("thename",thename)
                
                line=f'{cid}, {thename}, {symbol}'
                line_list.append(line)
            except:
                pass
        for line in line_list:
            this_csv_file.write(line)
            this_csv_file.write('\n')
def list_to_str(cid_list):
    cid_list=list(set(cid_list)) #cid_list is the list of ids from the csv file.
    the_cid_list=[int(value) for value in cid_list]
    cid_list_str = str(the_cid_list)[1:-1] #This eliminates the [brackets around the list
    cid_list_str=cid_list_str.replace(', ', ',').replace(' ,',',') 
#This eliminates the spaces before or after each comma.
    return cid_list_str

def test3():
    cid_list=[5015,11145,25417,4943,825,3408]
    cid_list_str=list_to_str(cid_list)
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?convert=USD'
    data=call_url(url,cid_list_str)
    for cid in cid_list:
        cid=str(cid)
        # pp.pprint(data['data'][cid])
        pp.pprint(data['data'][cid]['symbol'])
        # pp.pprint(data['data'][cid]['platform']['token_address'])
        pp.pprint(data['data'][cid]['quote']['USD']['price'])





if __name__ == "__main__":
    # test2()
    test3()