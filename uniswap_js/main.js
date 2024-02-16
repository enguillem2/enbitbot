const {ethers} = require("ethers")
const { join } = require("path")
const { ChainMismatchError } = require("web3")
const rpc_pulse='https://rpc.pulsechain.com'
const RPC_ETHEREUM="https://mainnet.infura.io/v3/fb6a702d37bc46cd988b5dd8dbf61ffd"
const provider = new ethers.providers.JsonRpcProvider(rpc_pulse)

const QuoterAbi = require('@uniswap/v3-periphery/artifacts/contracts/lens/Quoter.sol/Quoter.json').abi
var fs = require('fs')

//read file //////////////////////
function getFile(fPath){

    // try{
        const data=fs.readFileSync(fPath,'utf8')
        return data
    // }catch(err){
        // console.log(err)
        // return []
    // }
}
const abiPair = [
    "function token0() external view returns (address)",
    "function token1() external view returns (address)",
    "function fee() external view returns (uint24)"
  ]

const abiERC20 = [
    "function name() view returns (string)",
    "function decimals() view returns (uint8)",
    "function symbol() view returns (string)",
    "function balanceOf(address a) view returns (uint)",
  ]


async function getPrice(factory,amountIn,tradeDirection){
    
    const address = factory
    const pairContract = new ethers.Contract(address,abiPair,provider)
    let token0 = await pairContract.token0()
    let token1 = await pairContract.token1()
    let fee = await pairContract.fee()
    
    const token0Contract = new ethers.Contract(token0,abiERC20,provider)
    let decimals0=await token0Contract.decimals()
    let symbol0=await token0Contract.symbol()

    
    const token1Contract = new ethers.Contract(token1,abiERC20,provider)
    let decimals1=await token1Contract.decimals()
    let symbol1=await token1Contract.symbol()


    console.log("pair fee",fee)
    console.log("token0",token0,"symbol0",symbol0,"decimals0",decimals0)
    console.log("token1",token1,"symbol1",symbol1,"decimals1",decimals1)

}

//get file
async function getDepth(amountIn,limit){
    //get json surface rates
    console.log("reading surface informations")
    let fileInfo = getFile("../json/3uniswap_surface_rates.json")
    //5pulsex_surface_rates.json
    // let fileInfo = getFile("../json/5pulsex_surface_rates.json")
    fileJsonArray = JSON.parse(fileInfo)
    fileJsonArrayLimit = fileJsonArray.slice(0,limit)

    //loop through each price 
    for (let i=0; i <fileJsonArrayLimit.length;i++){
        //extract the variable
        let pair1ContractAdress= fileJsonArray[i].poolContract1
        let pair2ContractAdress= fileJsonArray[i].poolContract2
        let pair3ContractAdress= fileJsonArray[i].poolContract3

        let trade1Direction = fileJsonArray[i].poolDirectionTrade1
        let trade2Direction = fileJsonArray[i].poolDirectionTrade2
        let trade3Direction = fileJsonArray[i].poolDirectionTrade3

        //trade 1
        console.log("chechikig trade 1")

        let acquiredCoinDetailT1=await getPrice(pair1ContractAdress,amountIn,trade1Direction)

        




    }

}

getDepth(amountIn=1,limit=1)
//data=getFile("../json/3uniswap_surface_rates.json")
//console.log(data)