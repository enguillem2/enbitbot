const {ethers} = require("ethers")
const { join } = require("path")
const { ChainMismatchError } = require("web3")
const rpc_pulse='https://rpc.pulsechain.com'
const RPC_ETHEREUM="https://mainnet.infura.io/v3/fb6a702d37bc46cd988b5dd8dbf61ffd"
const provider = new ethers.providers.JsonRpcProvider(rpc_pulse)

const QuoterAbi = require('@uniswap/v3-periphery/artifacts/contracts/lens/Quoter.sol/Quoter.json').abi
var fs = require('fs')
const { getSystemErrorMap } = require("util")

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


async function getPrice(factory,amIn,tradeDirection){

    const address = factory
    let tokenInfoArray=[]
    let addressArray=[]
    let token0=""
    let token1=""
    let fee=""
    try{
        //get pool information
        const pairContract = new ethers.Contract(address,abiPair,provider)
        token0 = await pairContract.token0()
        token1 = await pairContract.token1()
        fee = await pairContract.fee()
        addressArray=[token0,token1]
    }catch(err){
        return 0
    }
    for (let i=0;i<addressArray.length;i++){
        //get individual token information
        const tokenContract = new ethers.Contract(addressArray[i],abiERC20,provider)
        let decimals=await tokenContract.decimals()
        let symbol=await tokenContract.symbol()
        let name=await tokenContract.name()
        let obj={
            id: "token"+1,
            tokenSymbol:symbol,
            tokenName:name,
            tokenDecimals:decimals,
            tokenAddress:addressArray[i]
        }
        tokenInfoArray.push(obj)
    }

    //identify the correct as A and B
    let inputTokenA=''
    let inputDecimalsA=0
    let inputTokenB=''
    let inputDecimalsB=0
    let factorA=0
    let factorB=0
    if (tradeDirection=="baseToQuote"){
        inputTokenA=tokenInfoArray[0].tokenAddress
        inputDecimalsA=tokenInfoArray[0].tokenDecimals
        
        inputTokenB=tokenInfoArray[1].tokenAddress
        inputDecimalsB=tokenInfoArray[1].tokenDecimals
    }
    
    if (tradeDirection=="quoteToBase"){
        inputTokenA=tokenInfoArray[1].tokenAddress
        inputDecimalsA=tokenInfoArray[1].tokenDecimals
        
        inputTokenB=tokenInfoArray[0].tokenAddress
        inputDecimalsB=tokenInfoArray[0].tokenDecimals
    }
    factorA = Math.pow(10,inputDecimalsA)
    factorB = Math.pow(10,inputDecimalsB)


    //reformat Amount in
    if(!isNaN(amIn)){amIn=amIn.toString()}
    let amountIn = ethers.utils.parseUnits(amIn,inputDecimalsA).toString()

    //get uniswap v3 quote
    //https://docs.uniswap.org/contracts/v3/reference/deployments
    const quoterAddress ="0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
    const quoterContract=new ethers.Contract(quoterAddress,QuoterAbi,provider)
    let quotedAmountOut=0
    try{
        quotedAmountOut= await quoterContract.callStatic.quoteExactInputSingle(
            inputTokenA,
            inputTokenB,
            fee,
            amountIn,
            0
        )
        let outPutAmount= ethers.utils.formatUnits(quotedAmountOut,inputDecimalsB).toString()
        // console.log("outPutAmount",outPutAmount)
        return outPutAmount

    }catch(err){
        return 0
    }
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
        let acquiredCoinT1=await getPrice(pair1ContractAdress,amountIn,trade1Direction)

        if (acquiredCoinT1!=0){
            //trade 2
            console.log("checking trade 2")
            let acquiredCoinT2=await getPrice(pair2ContractAdress,acquiredCoinT1,trade2Direction)


            if (acquiredCoinT2!=0){
                //trade 2
                console.log("checking trade 3")
                let acquiredCoinT3=await getPrice(pair3ContractAdress,acquiredCoinT2,trade3Direction)
                console.log(amountIn,acquiredCoinT3)
            }
        }



        




    }

}

getDepth(amountIn=1,limit=30)
//data=getFile("../json/3uniswap_surface_rates.json")
//console.log(data)