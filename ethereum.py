from config import *
from abis import *
from contracts import *

def get_balance(address,provider=w3_pulse):
    print(address)
    X=provider.eth.get_balance(address)
    decimals=18
    factor=10**decimals
    X=X/factor
    return float(X)

def get_token_balance(token_address,who_address,abi=erc20_abi,provider=w3_pulse):
    token = provider.eth.contract(address=token_address,abi=erc20_abi)
    decimals=token.functions.decimals().call()
    factor=10**decimals
    X=token.functions.balanceOf(who_address).call()/factor
    return float(X)

def get_pair_price(address_from, 
                   address_to,
                   provider=w3_pulse,
                   router_address=router_address_pulse,
                   amount=1
                   ):
    amount_ini=round(amount)
    router_contract = provider.eth.contract(address=router_address, abi=router_abi)

    address_from_contract = provider.eth.contract(address=address_from,abi=erc20_abi)
    decimals_from=address_from_contract.functions.decimals().call()
    name_from=address_from_contract.functions.name().call()
    symbol=address_from_contract.functions.symbol().call()


    address_to_contract = provider.eth.contract(address=address_to,abi=erc20_abi)
    decimals_to = address_to_contract.functions.decimals().call()
    factor_from=10**decimals_from
    factor_to=10**decimals_to

    amount_ini=amount_ini*factor_from
    
    get_prices=router_contract.functions.getAmountsOut(amount_ini,[address_from,address_to]).call()
    return {"symbol":symbol,"price":get_prices[1]/factor_to}