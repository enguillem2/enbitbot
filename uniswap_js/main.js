const {ethers} = require("ethers")
const rpc_pulse='https://rpc.pulsechain.com'
const RPC_ETHEREUM="https://mainnet.infura.io/v3/fb6a702d37bc46cd988b5dd8dbf61ffd"
const provider = new ethers.providers.JsonRpcProvider(rpc_pulse)
