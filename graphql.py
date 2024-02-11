#https://graph.pulsechain.com/subgraphs/name/pulsechain/blocks/graphql?query=%0A++++%23%0A++++%23+Welcome+to+The+GraphiQL%0A++++%23%0A++++%23+GraphiQL+is+an+in-browser+tool+for+writing%2C+validating%2C+and%0A++++%23+testing+GraphQL+queries.%0A++++%23%0A++++%23+Type+queries+into+this+side+of+the+screen%2C+and+you+will+see+intelligent%0A++++%23+typeaheads+aware+of+the+current+GraphQL+type+schema+and+live+syntax+and%0A++++%23+validation+errors+highlighted+within+the+text.%0A++++%23%0A++++%23+GraphQL+queries+typically+start+with+a+%22%7B%22+character.+Lines+that+start%0A++++%23+with+a+%23+are+ignored.%0A++++%23%0A++++%23+An+example+GraphQL+query+might+look+like%3A%0A++++%23%0A++++%23+++++%7B%0A++++%23+++++++field%28arg%3A+%22value%22%29+%7B%0A++++%23+++++++++subField%0A++++%23+++++++%7D%0A++++%23+++++%7D%0A++++%23%0A++++%23+Keyboard+shortcuts%3A%0A++++%23%0A++++%23++Prettify+Query%3A++Shift-Ctrl-P+%28or+press+the+prettify+button+above%29%0A++++%23%0A++++%23+++++Merge+Query%3A++Shift-Ctrl-M+%28or+press+the+merge+button+above%29%0A++++%23%0A++++%23+++++++Run+Query%3A++Ctrl-Enter+%28or+press+the+play+button+above%29%0A++++%23%0A++++%23+++Auto+Complete%3A++Ctrl-Space+%28or+just+start+typing%29%0A++++%23%0A++
import requests
import json
from func_triangular_arg import structure_trading_pairs


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

if __name__ == "__main__":
    pairs=retrieve_uniswap_information()
    structured_pairs=structure_trading_pairs(pairs["data"]["pools"],limit=200)
    print(len(structured_pairs))