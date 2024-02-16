const {ethers} = require("ethers")
const rpc_pulse='https://rpc.pulsechain.com'
const RPC_ETHEREUM="https://mainnet.infura.io/v3/fb6a702d37bc46cd988b5dd8dbf61ffd"
const provider = new ethers.providers.JsonRpcProvider(rpc_pulse)

const abi = [
    "function name() view returns (string)",
    "function decimals() view returns (uint8)",
    "function symbol() view returns (string)",
    "function balanceOf(address a) view returns (uint)"
  ]

const address = '0x95B303987A60C71504D99Aa1b13B4DA07b0790ab'
const tokenContract = new ethers.Contract(address,abi,provider)

async function getDetails(){
  let tokenName = await tokenContract.name()
  let symbol = await tokenContract.symbol()
  let decimals = await tokenContract.decimals()
  let balanceOf=await tokenContract.balanceOf("0xebBC1EEf2F64604bdC0C72AF50F17f71B879d0b6")
  let factor= Math.pow(10,decimals)
  balanceOf=Number(balanceOf)/factor

  console.log(tokenName,symbol,decimals)
  console.log(balanceOf)
}

getDetails()