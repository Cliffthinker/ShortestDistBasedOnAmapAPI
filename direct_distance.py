import requests as re
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  
import networkx as nx    

mykey = '70a897d6dd09533575951e02effb151a'
search_url='http://restapi.amap.com/v3/place/text'
s_param={
    'key':mykey,
    'keywords':'大学',
    'types':'高等院校',
    'city':'北京',
    'children':'1',
    'offset':'30',
    'page':'1',
    'extensions':'all'
}
cam_r = re.get(search_url,params=s_param)
cam_r.encoding = 'utf-8'
r_json=cam_r.json()

cam_names=[]
cam_location=[]
for i in range(30):
    cam_names.append(r_json["pois"][i]["name"])
    loc_str=r_json["pois"][i]["location"]
    loc=tuple(map(float,loc_str.split(',')))
    cam_location.append(loc)
    # cam_location.append(r_json["pois"][i]["location"])

print(cam_names)
for each in cam_location:
    print(each)

R=6370
dist_mat=[[0 for i in range(30)] for i in range(30)]
for i in range(30):
    for j in range(i+1,30):
        x1=cam_location[i][0]
        x2=cam_location[j][0]
        y1=cam_location[i][1]
        y2=cam_location[j][1]
        dist_mat[i][j]=R* np.arccos(np.sin(y1)*np.sin(y2)+np.cos(y1)*np.cos(y2)*np.cos(x1-x2)) 
print(dist_mat)

for i in range(30):
    for j in range(0,i):
        dist_mat[i][j]=dist_mat[j][i]

dist_mat=np.array(dist_mat)
dist_df=pd.DataFrame(dist_mat,index=cam_names,columns=cam_names)
filename = pd.ExcelWriter('direct_distance_data.xlsx')
dist_df.to_excel(filename,sheet_name="Distance")

graph = nx.from_numpy_matrix(dist_mat)

for it in range(30):
    i0=0
    length = nx.dijkstra_path_length(graph,source=i0,target=it)
    path = nx.dijkstra_path(graph,source=i0,target=it)
    # nx.draw_networkx(graph)
    # plt.show()
    print(length)
    print(path)
    path_str=''
    for each in path:
        path_str += cam_names[each]+'->'
    print(path_str)
        