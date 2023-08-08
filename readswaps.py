import os
import time
from functools import lru_cache

from web3 import HTTPProvider, Web3

from eth_defi.abi import get_contract
# from eth_defi.chain import install_chain_middleware
from eth_defi.event_reader.filter import Filter
# from eth_defi.event_reader.logresult import decode_log
from eth_defi.event_reader.reader import read_events, LogResult
from eth_defi.uniswap_v2.pair import fetch_pair_details, PairDetails

from config import *


QUOTE_TOKENS = ["BUSD", "USDC", "USDT"]

@lru_cache(maxsize=100)
def fetch_pair_details_cached(web3: Web3, pair_address: str) -> PairDetails:
    return fetch_pair_details(web3, pair_address)


def main():
    json_rpc_url = os.environ.get("JSON_RPC_BINANCE", "https://bsc-dataseed.binance.org/")
    web3 = Web3(HTTPProvider(json_rpc_url))
    web3.middleware_onion.clear()

    # Read the prepackaged ABI files and set up event filter
    # for any Uniswap v2 like pool on BNB Smart Chain (not just PancakeSwap).
    #
    # We use ABI files distributed by SushiSwap project.
    #
    Pair = get_contract(web3, "sushi/UniswapV2Pair.json")


if __name__ == "__main__":
    main()