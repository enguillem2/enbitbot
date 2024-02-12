#https://graph.pulsechain.com/subgraphs/name/pulsechain/blocks/graphql?query=%0A++++%23%0A++++%23+Welcome+to+The+GraphiQL%0A++++%23%0A++++%23+GraphiQL+is+an+in-browser+tool+for+writing%2C+validating%2C+and%0A++++%23+testing+GraphQL+queries.%0A++++%23%0A++++%23+Type+queries+into+this+side+of+the+screen%2C+and+you+will+see+intelligent%0A++++%23+typeaheads+aware+of+the+current+GraphQL+type+schema+and+live+syntax+and%0A++++%23+validation+errors+highlighted+within+the+text.%0A++++%23%0A++++%23+GraphQL+queries+typically+start+with+a+%22%7B%22+character.+Lines+that+start%0A++++%23+with+a+%23+are+ignored.%0A++++%23%0A++++%23+An+example+GraphQL+query+might+look+like%3A%0A++++%23%0A++++%23+++++%7B%0A++++%23+++++++field%28arg%3A+%22value%22%29+%7B%0A++++%23+++++++++subField%0A++++%23+++++++%7D%0A++++%23+++++%7D%0A++++%23%0A++++%23+Keyboard+shortcuts%3A%0A++++%23%0A++++%23++Prettify+Query%3A++Shift-Ctrl-P+%28or+press+the+prettify+button+above%29%0A++++%23%0A++++%23+++++Merge+Query%3A++Shift-Ctrl-M+%28or+press+the+merge+button+above%29%0A++++%23%0A++++%23+++++++Run+Query%3A++Ctrl-Enter+%28or+press+the+play+button+above%29%0A++++%23%0A++++%23+++Auto+Complete%3A++Ctrl-Space+%28or+just+start+typing%29%0A++++%23%0A++
import requests
import json
from func_triangular_arg import structure_trading_pairs,calc_triangular_arb_surface_rate
from pulsexread import get_all_pairs
import pickle


def retriev_pulsex_w3():
    pairs=get_all_pairs()
    print(f"len paris {len(pairs)}")

def retriev_pulsex_information():
    query="""

        {
  pairs (orderBy: reserveUSD orderDirection:desc first:500) {
    id
    reserveUSD
    reserve0
    reserve1
    token0 {
      id
      name      
      decimals
      symbol
    }
    token0Price
    token1 {
      id
      name     
      decimals
      symbol
    }    
    token1Price
  }
}
    """
    url="https://graph.pulsechain.com/subgraphs/name/pulsechain/pairs"
    url="https://graph.pulsechain.com/subgraphs/name/pulsechain/pulsex"
    req = requests.post(url,json={'query':query})
    json_dict =json.loads(req.text)
    return json_dict


def retrieve_uniswap_information():
    query="""
        {
        pools(orderBy: totalValueLockedETH,
                    orderDirection: desc,
                    first:500){
                        id
                        totalValueLockedETH
                        token0Price
                        token1Price
                        feeTier
                        token0{id symbol name decimals}
                        token1{id symbol name decimals}
        }
        }
    """
    url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
    req = requests.post(url,json={'query':query})
    json_dict =json.loads(req.text)
    return json_dict

def conect_to_uniswap(load_from_blockchain=True):
    structured_pairs=[]
    file_name="structured_pairs_uniswap.pkl"
    if load_from_blockchain:
        pairs=retrieve_uniswap_information()
        the_pairs=pairs["data"]["pools"]
        the_limit=len(the_pairs)
        structured_pairs=structure_trading_pairs(the_pairs,limit=the_limit)
        with open(f"pkl/{file_name}.pkl", "wb") as f:
            pickle.dump(structured_pairs, f)
    else:
        structured_pairs = pickle.load( open(f"pkl/{file_name}.pkl", "rb" ))

    print(len(structured_pairs))

    for t_pair in structured_pairs:
        calc_triangular_arb_surface_rate(t_pair)

def conect_to_pulsex(load_from_blockchain=True):
    structured_pairs=[]
    if load_from_blockchain:
        pairs=retriev_pulsex_information()
        # print(pairs)
        the_pairs=pairs["data"]["pairs"]
        print(the_pairs[0:2])
        the_limit=len(the_pairs)
        print(f"pairs: {len(the_pairs)}")
        # print(the_pairs[0])
        structured_pairs=structure_trading_pairs(the_pairs,limit=the_limit)
        with open("pkl/structured_pairs_pls.pkl", "wb") as f:
            pickle.dump(structured_pairs, f)
    else:
        #load from pickle
        structured_pairs = pickle.load( open("pkl/structured_pairs_pls.pkl", "rb" ))

    print(len(structured_pairs))
    
    for t_pair in structured_pairs:
        surf_rate=calc_triangular_arb_surface_rate(t_pair,min_rate=1.5)
        print(f"{surf_rate} ")


    # retriev_pulsex_w3()
    # print(structured_pairs)

    

if __name__ == "__main__":
    # conect_to_uniswap(load_from_blockchain=False)
    conect_to_pulsex(load_from_blockchain=True)