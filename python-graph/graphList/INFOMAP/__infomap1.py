import infomap
import pandas as pd
from flask import current_app




def runinfomap(G):
    '''
    Run Infomap on a networkx graph
    :param G: networkx graph
    :return:
    '''
    current_app.logger.info("Running Infomap...")


    infomapWrapper = infomap.Infomap("--two-level --directed",silent=True)
    mapping = infomapWrapper.add_networkx_graph(G,weight='weight')
    # print(mapping)

    print("Find communities with Infomap...")
    infomapWrapper.run()


    print(f"Found {infomapWrapper.num_top_modules} modules with codelength: {infomapWrapper.codelength}")

    print("Result")
    print("\n#node module")
    # 汇总df
    result_list = []
    for node in infomapWrapper.tree:
        if node.is_leaf:
            # print(node.node_id, node.module_id)
            result_list.append([mapping.get(node.node_id),node.module_id])

    df = pd.DataFrame(result_list,columns=['clue','module'])
    print(df)
    print(df['module'].value_counts())



    return df
