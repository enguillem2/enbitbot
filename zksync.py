from config import *
from abis import *
from contracts import *
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.manage_contracts.nonce_holder import NonceHolder

from eth_account import Account
from eth_account.signers.local import LocalAccount
from zksync2.signer.eth_signer import PrivateKeyEthSigner

account: LocalAccount = Account.from_key(pk_mainnet)

web3 = ZkSyncBuilder.build(RPC_ZKSYNC)

account = Account.from_key(pk_mainnet)
zksync_web3 = ZkSyncBuilder.build(RPC_ZKSYNC)

chain_id = zksync_web3.zksync.chain_id
signer = PrivateKeyEthSigner(account, chain_id)
nonce_holder = NonceHolder(zksync_web3, account)

QUOTE_TOKEN_ADDRESS = "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C"  # BUSD

# The address of a token we are going to receive
#
# Use https://tradingstrategy.ai/search to find your token
#
# For base terminology see https://tradingstrategy.ai/glossary/base-token
BASE_TOKEN_ADDRESS = "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4"  # Binance custodied ETH on BNB Chain


def approve(token, spender_address, wallet_address, private_key):

  spender = spender_address
  max_amount = web3.to_wei(2**64-1,'ether')
  nonce = web3.eth.get_transaction_count(wallet_address)

  tx = token.functions.approve(spender, max_amount).build_transaction({
      'from': wallet_address, 
      'nonce': nonce
      })
    
  signed_tx = web3.eth.account.signTransaction(tx, private_key)
  tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

  return web3.toHex(tx_hash)

if __name__ == "__main__":
    quote_token = web3.eth.contract(address=QUOTE_TOKEN_ADDRESS,abi=erc20_abi)

    approve(quote_token,"0x5aEaF2883FBf30f3D62471154eDa3C0c1b05942d",address_airdrops,pk_mainnet)

    print("hello",web3)
    print("account: ",account)
    print(f"chain_id {chain_id} signer: {signer}")
    print(f"nonce: {nonce_holder}")
    print(f"quote token {quote_token}")