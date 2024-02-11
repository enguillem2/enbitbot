#structured tradign pai groups

def structure_trading_pairs(pairs,limit=100):
    triangular_pairs_list=[]
    remove_duplicates_list=[]
    pairs_list = pairs[:limit]

    for pair_a in pairs_list:
        #get first pair (A)
        a_base=pair_a["token0"]["symbol"]
        a_quote=pair_a["token1"]["symbol"]
        a_pair =f"{a_base}_{a_quote}"
        a_token_0_id = pair_a["token0"]["id"]
        a_token_1_id = pair_a["token1"]["id"]
        a_contract = pair_a["id"]
        a_token_0_decimals=pair_a["token0"]["decimals"]
        a_token_1_decimals=pair_a["token1"]["decimals"]
        a_token_0_price=pair_a["token0Price"]
        a_token_1_price=pair_a["token1Price"]

        #put (A into a box for checking at b
        a_pair_box=[a_base,a_quote]

        #Get second pair (B)
        for pair_b in pairs_list:
            b_base=pair_b["token0"]["symbol"]
            b_quote=pair_b["token1"]["symbol"]
            b_pair =f"{b_base}_{b_quote}"
            b_token_0_id = pair_b["token0"]["id"]
            b_token_1_id = pair_b["token1"]["id"]
            b_contract = pair_b["id"]
            b_token_0_decimals=pair_b["token0"]["decimals"]
            b_token_1_decimals=pair_b["token1"]["decimals"]
            b_token_0_price=pair_b["token0Price"]
            b_token_1_price=pair_b["token1Price"]

            #get third paid (c)
            if a_pair != b_pair:
                if b_base in a_pair_box or b_quote in a_pair_box:
                    #get third pair (C)
                    for pair_c in pairs_list:
                        c_base=pair_c["token0"]["symbol"]
                        c_quote=pair_c["token1"]["symbol"]
                        c_pair =f"{c_base}_{c_quote}"
                        c_token_0_id = pair_c["token0"]["id"]
                        c_token_1_id = pair_c["token1"]["id"]
                        c_contract = pair_c["id"]
                        c_token_0_decimals=pair_c["token0"]["decimals"]
                        c_token_1_decimals=pair_c["token1"]["decimals"]
                        c_token_0_price=pair_c["token0Price"]
                        c_token_1_price=pair_c["token1Price"]

                        #count number on (C) items
                        if c_pair != a_pair and c_pair != b_pair:
                            combine_all = [a_pair,b_pair,c_pair]
                            pair_box = [a_base,a_quote,b_base,b_quote,c_base,c_quote]

                            counts_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    counts_c_base+=1

                            counts_c_quote=0
                            for i in pair_box:
                                if i == c_quote:
                                    counts_c_quote+=1

                            if counts_c_base == 2 and counts_c_quote  == 2 and c_base != c_quote:
                                combined = a_pair+","+b_pair+","+c_pair
                                unique_string = "".join(sorted(combined))

                                #ouput pair
                                if unique_string not in remove_duplicates_list:
                                    output_dict = {
                                        "aPair":a_pair,
                                        "aBase":a_base,
                                        "aQuote":a_quote,
                                        "bPair":b_pair,
                                        "bBase":b_base,
                                        "bQuote":b_quote,
                                        "cPair":c_pair,
                                        "cBase":c_base,
                                        "cQuote":c_quote,
                                        "combined":combined,
                                        "aToken0Id":a_token_0_id,
                                        "bToken0Id":b_token_0_id,
                                        "cToken0Id":c_token_0_id,
                                        "aToken1Id":a_token_1_id,
                                        "bToken1Id":b_token_1_id,
                                        "cToken1Id":c_token_1_id,
                                        "aContract":a_contract,
                                        "bContract":b_contract,
                                        "cContract":c_contract,
                                        "aToken0Decimals":a_token_0_decimals,
                                        "bToken0Decimals":b_token_0_decimals,
                                        "cToken0Decimals":c_token_0_decimals,
                                        "aToken1Decimals":a_token_1_decimals,
                                        "bToken1Decimals":b_token_1_decimals,
                                        "cToken1Decimals":c_token_1_decimals,
                                        "aToken0Price":a_token_0_price,
                                        "bToken0Price":b_token_0_price,
                                        "cToken0Price":c_token_0_price,
                                        "aToken1Price":a_token_1_price,
                                        "bToken1Price":b_token_1_price,
                                        "cToken1Price":c_token_1_price
                                    }
                                    triangular_pairs_list.append(output_dict)
                                    remove_duplicates_list.append(unique_string)
    return triangular_pairs_list








