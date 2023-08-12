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
        'ANKR,REV,NPXS,VGX,FTM,CHSB,REN,IOST,BTMX,CELO,PAX,CFX'))
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

if __name__ == "__main__":
    test2()