from pyserver.common.action import base
import numpy as np
import pandas as pd
import pymysql
from .classify import read_node_label, Classifier
from .node2vec import Node2Vec
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.manifold import TSNE
import warnings
warnings.filterwarnings('ignore')



def evaluate_embeddings(embeddings,x,y):
    X, Y = x,y
    tr_frac = 0.8
    print("Training classifier using {:.2f}% nodes...".format(
        tr_frac * 100))
    clf = Classifier(embeddings=embeddings, clf=LogisticRegression())
    clf.split_train_evaluate(X, Y, tr_frac)


def plot_embeddings(embeddings,x,y):
    X, Y = x,y

    emb_list = []
    for k in X:
        emb_list.append(embeddings[k])
    emb_list = np.array(emb_list)

    model = TSNE(n_components=2)
    node_pos = model.fit_transform(emb_list)

    color_idx = {}
    for i in range(len(X)):
        color_idx.setdefault(Y[i][0], [])
        color_idx[Y[i][0]].append(i)

    for c, idx in color_idx.items():
        plt.scatter(node_pos[idx, 0], node_pos[idx, 1], label=c)
    plt.legend()
    plt.show()

def query_sql(cursor,sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    col = [item[0] for item in cursor.description]
    return res,col

def get_engine():
    #         mysql+pymysql://{account}:{password}@{host}:{port}/{dbName}?charset=utf8
    engine = 'mysql+pymysql://root:123456@172.30.6.63:3306/test1?charset=utf8'
    return engine

class node2vecter(base):
    def process(self):
        connection = pymysql.connect(host='172.30.6.63', user='root', password='123456', database='test1',
                                     port=int(3306))
        try:
            with connection.cursor() as cursor:
                sql = '''
                    select *
                    from Wiki_edgelist
                '''
                data, columns = query_sql(cursor, sql)
                graph_feature = pd.DataFrame(data, columns=columns)
                sql = '''
                    select *
                    from wiki_labels
                
                '''
                data, columns = query_sql(cursor, sql)
                graph_labels = pd.DataFrame(data, columns=columns)
        finally:
            connection.close()
        x = graph_labels.values[0]
        y = graph_labels.values[1]

        G = nx.read_edgelist(graph_feature,
                             create_using=nx.DiGraph(), nodetype=None, data=[('weight', int)])
        model = Node2Vec(G, walk_length=10, num_walks=80,
                         p=0.25, q=4, workers=1, use_rejection_sampling=0)
        model.train(window_size=5, iter=3)
        embeddings = model.get_embeddings()

        evaluate_embeddings(embeddings,x,y)
        # plot_embeddings(embeddings,x,y)



if __name__ == "__main__":
    action = node2vecter()
    action.process()


