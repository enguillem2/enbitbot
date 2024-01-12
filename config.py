from decouple import config
from web3 import Web3, HTTPProvider

RPC_ETHEREUM=config("RPC_ETHEREUM")
RPC_GOERLI=config("RPC_GOERLI")

RPC_PULSE=config("RPC_PULSE")
RPC_PULSE_TESTNET=config("RPC_PULSE_TESTNET")

RPC_BSC=config("RPC_BSC")
RPC_BSC_TESTNET=config("RPC_BSC_TESTNET")

RPC_ZKSYNC=config("RPC_ZKSYNC")

RPC_POLYGON=config("RPC_POLYGON")

w3_ethereum=Web3(HTTPProvider(RPC_ETHEREUM))
w3_goerli=Web3(HTTPProvider(RPC_GOERLI))

w3_pulse =Web3(HTTPProvider(RPC_PULSE))
w3_pulse_testnet=Web3(HTTPProvider(RPC_PULSE_TESTNET))

w3_bsc=Web3(HTTPProvider(RPC_BSC))
w3_bsc_testnet=Web3(HTTPProvider(RPC_BSC_TESTNET))


w3_zksync=Web3(HTTPProvider(RPC_ZKSYNC))

w3_polygon=Web3(HTTPProvider(RPC_POLYGON))


TELEGRAM_TOKEN=config("TELEGRAM_TOKEN")
CID_CANAL_TESTS=config("CID_CANAL_TESTS")

TELEGRAM_ENBITBOT=config("TELEGRAM_ENBITBOT")

address_airdrops=config("address_airdrops")
pk_mainnet=config("pk_mainnet")
pk_mainnet_ox="0x"+pk_mainnet
address_brave=config("address_brave")

key_cmc=config("COINMARKETCAP_API_KEY")