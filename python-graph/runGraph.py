# encoding: utf-8
import os
from graphList.LOUVAIN.__louvain import runlouvain
from graphList.INFOMAP.__infomap import Infomap
from graphList.INFOMAP.__infomap1 import runinfomap
from flask import Flask,request,url_for,g,session,jsonify
from common.log import applog
import logging
from createGraph.create_Graph import creat_graph
import pandas as pd
from createGraph.create_Graph_new import creat_nx_graph
from createGraph import create_Graph_new as cg
import sys
import time
from graphList.evaluation_graph.centrality_community import centrality_community_with_degree,centrality_community_with_shortest_path
from graphList.evaluation_graph.tightness_community import tightness_community_with_graph



app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.register_blueprint(creat_graph,url_prefix='/pythonGraph/creat',)
# 日志
log_handler = applog.get_handler(os.path.dirname(__file__))
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)





# 在每个请求之前执行
@app.before_request
@app.route('/pythonGraph/init/initGraph', methods=['get', 'post'])
def before_request():
    '''
    :return:    None
    '''
    app.logger.info('执行before_request')

    # 记录开始时间
    g.stdt = time.time()



# 在每个请求之后执行
@app.after_request
def after_request(response):
    '''
    :param response:
    :return:
    '''
    app.logger.info('执行after_request')

    # 接收上一个请求的响应  可以对响应进行处理
    new_respose = app.make_response('return ok')
    new_respose.status_code = 200

    return response



# http://127.0.0.1:5000/pythonGraph/run/louvain?resolution=1&threshold=0.000001
@app.route('/pythonGraph/run/louvain',methods=['get','post'])
def run_louvain():
    '''
    :param resolution: 社区规模，大于1算法更倾向于筛选出更大的社区
    :param threshold: 模块化增益阈值，算法在合并社区时的模块化增益小于阈值则停止算法
    :param a1: 算法参数1
    :param a2: 算法参数2
    :param a3: 算法参数3
    :return: 算法结果
    '''
    app.logger.info('louvain开始！')


    # 获取接口参数
    # 社区规模，大于1算法更倾向于筛选出更大的社区
    resolution = int(request.args.get('resolution'))
    # 模块化增益阈值，算法在合并社区时的模块化增益小于阈值则停止算法
    threshold = float(request.args.get('threshold'))
    # a1 = request.form.get('a1')
    # a2 = request.form.get('a2')
    # a3 = request.form.get('a3')


    # 创建networkx图
    G = cg.creat_nx_graph()
    app.logger.info('图创建成功！')
    app.logger.info(f'{G.number_of_nodes()}节点，{G.number_of_edges()}边')


    # louvain算法调用
    community_louvain,community_louvain_info = runlouvain(G,resolution,threshold)
    app.logger.info(f'LOUVAIN运行结果：\n{community_louvain}')
    app.logger.info(f'louvain各社区结果详情：\n{community_louvain_info}')


    # 评估算法效果
    # 基于度的中心性评估
    graph_evaluation_with_degree = centrality_community_with_degree(G)
    # 基于最短路径的中心性评估
    graph_evaluation_with_shortest_path = centrality_community_with_shortest_path(G)
    # 社区紧密度评估
    graph_evaluation_with_tightness = tightness_community_with_graph(G)


    # 记录结束时间
    eddt = time.time()
    app.logger.info(f'louvain耗时：{eddt-g.stdt}')


    # 返回团伙及评估指标
    return jsonify({'community_louvain':community_louvain,'graph_evaluation_with_degree':graph_evaluation_with_degree})





# http://127.0.0.1:5000/pythonGraph/run/infomap
@app.route('/pythonGraph/run/infomap', methods=['get', 'post'])
def run_infomap():
    '''
    :param
    :return:
    '''
    app.logger.info('infomap开始！')

    # 获取接口参数
    xxx = request.args.get('xxx')


    # infomap算法调用
    community_infomap = Infomap(globals_G).printCom(globals_G)

    return 'infomap ok'




# http://127.0.0.1:5000/pythonGraph/run/infomap1
@app.route('/pythonGraph/run/infomap1', methods=['get', 'post'])
def run_infomap1():


    # 调库infomap实现
    community_infomap1 = runinfomap(globals_G)

    return 'infomap1 ok'




@app.route('/pythonGraph/run/lpa', methods=['get', 'post'])
def run_lpa():

    pass

    return 'lpa ok'








if __name__ == '__main__':

    app.run(debug=True)








