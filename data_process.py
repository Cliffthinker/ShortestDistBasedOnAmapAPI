import matplotlib.pyplot as plt  
import networkx as nx    
import pandas as pd
import numpy as np

def str2set(str):
    s_list=str[1:len(str)-1].split(',')
    s_new_list=[]
    for each in s_list:
        s_new_list.append(each.split("'")[1])
    return set(s_new_list)

filename = '公交站数据\\dist_dura_data.xlsx'
df = pd.read_excel(filename,0)
dist_data =df.values
graph = nx.from_numpy_matrix(dist_data)
bus_df=pd.read_excel('公交站数据\\data.xlsx')
bus=bus_df.values[:,1].tolist()
bus_set=list(map(str2set,bus))

for it in range(50):
    i0=7
    length = nx.dijkstra_path_length(graph,source=i0,target=it)
    path = nx.dijkstra_path(graph,source=i0,target=it)
    # nx.draw_networkx(graph)
    # plt.show()
    print('最短路径长度：',length)
    print('最短路径：',path)
    cam_name_list=df.index
    path_str=''
    for each in path:
        path_str += cam_name_list[each]+'->'
    print(path_str[0:len(path_str)-2])
    bus_path=''
    for i in range(len(path)-1):
        bus_path += str(bus_set[path[i]]&bus_set[path[i+1]])+'->'
    print('公交车换乘:',bus_path[0:len(bus_path)-2])
    print("-------------------------------------------------------------")

        
