from math import *
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def TOPSIS(G1):
    betCent = nx.betweenness_centrality(G1)
    closCent = nx.closeness_centrality(G1)
    degCent = nx.degree_centrality(G1)
    eigCent = nx.eigenvector_centrality(G1)

    """# sort centrality measures"""

    BC = []
    DC = []
    EC = []
    CC = []

    for i in sorted(betCent):
        BC.append(betCent[i])

    for i in sorted(closCent):
        CC.append(closCent[i])

    for i in sorted(degCent):
        DC.append(degCent[i])

    for i in sorted(eigCent):
        EC.append(eigCent[i])

    #Creating data matrix
    mat = pd.DataFrame({'DC' : DC,
                        'CC' : CC,
                        'BC' : BC,
                        'EC' : EC})


    DC_denom = sqrt((mat['DC']**2).sum())
    CC_denom = sqrt((mat['CC']**2).sum())
    BC_denom = sqrt((mat['BC']**2).sum())
    EC_denom = sqrt((mat['EC']**2).sum())

    """##  Normalized matrix"""

    mat_norm = pd.DataFrame({
        'DC' : mat['DC'] / DC_denom,
        'CC' : mat['CC'] / CC_denom,
        'BC' : mat['BC'] / BC_denom,
        'EC' : mat['EC'] / EC_denom,
    })

    """# assign weights to criterion"""

    mat_norm_weighted = mat_norm

    mat_norm_weighted['DC'] = mat_norm_weighted['DC'] * 0.2
    mat_norm_weighted['EC'] = mat_norm_weighted['EC'] * 0.2
    mat_norm_weighted['BC'] = mat_norm_weighted['BC'] * 0.3
    mat_norm_weighted['CC'] = mat_norm_weighted['CC'] * 0.3

    """# determining Ideal best & worst"""

    DC_ideal_best = mat_norm_weighted['DC'].max()
    DC_ideal_worst = mat_norm_weighted['DC'].min()

    CC_ideal_best = mat_norm_weighted['CC'].max()
    CC_ideal_worst = mat_norm_weighted['CC'].min()

    BC_ideal_best = mat_norm_weighted['BC'].max()
    BC_ideal_worst = mat_norm_weighted['BC'].min()

    EC_ideal_best = mat_norm_weighted['EC'].max()
    EC_ideal_worst = mat_norm_weighted['EC'].min()

    """## S+ & S-"""

    mat_norm_weighted["from_best"] = (mat_norm_weighted["DC"] - DC_ideal_best)**2 + (mat_norm_weighted['CC'] - CC_ideal_best)**2 + (mat_norm_weighted['BC'] - BC_ideal_best)**2 + (mat_norm_weighted['EC'] - EC_ideal_best)**2
    mat_norm_weighted["from_worst"] = (mat_norm_weighted["DC"] - DC_ideal_worst)**2 + (mat_norm_weighted['CC'] - CC_ideal_worst)**2 + (mat_norm_weighted['BC'] - BC_ideal_worst)**2 + (mat_norm_weighted['EC'] - EC_ideal_worst)**2

    """## sqrt of distance"""

    mat_norm_weighted["from_best"] = mat_norm_weighted["from_best"].apply(lambda x : sqrt(x))
    mat_norm_weighted["from_worst"] = mat_norm_weighted["from_worst"].apply(lambda x : sqrt(x))

    """# Calculate the ratio"""

    mat_norm_weighted['ratio'] = mat_norm_weighted['from_worst'] / (mat_norm_weighted['from_worst'] + mat_norm_weighted['from_best'])

    """# save results"""

    result = mat

    result['TOPSIS'] = mat_norm_weighted['ratio']
    result.sort_values(by="TOPSIS", ascending=False ,inplace=True)

    result.reset_index(inplace=True)

    result.rename(columns={"index" : "node"}, inplace=True)

    # result.to_csv("TOPSIS_result.csv", index = False)

    return result