#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 10:48
# @Author  : RenTao
# @File    : get_dist_pos_data.py
# @Software: PyCharm

import requests as re
import time
import numpy as np
import pandas as pd
import os

def search_pos(key,keyword,save_folder):
    search_url='http://restapi.amap.com/v3/place/text'
    s_param={
        'key':key,
        'keywords':keyword,
        'types':'',
        'city':'北京',
        'children':'1',
        'offset':'50',
        'page':'1',
        'extensions':'all'
    }
    r = re.get(search_url,params=s_param)
    r.encoding = 'utf-8'
    r_json=r.json()

    names=[]
    location=[]
    address=[]
    # rand_index = random.sample([i for i in range(100)],30)
    for i in range(50):
        names.append(r_json["pois"][i]["name"])
        location.append(r_json["pois"][i]["location"])
        temp=r_json["pois"][i]["address"]
        address.append(set(temp.split(';')))
    print(names)
    for each in location:
        print(each)
    s_result=[location,address]
    print(s_result)
    df = pd.DataFrame(s_result,index=['location','address'],columns=names)
    print(df)
    filename=save_folder+'\\data.xlsx'
    df_T = df.T
    df_T.to_excel(filename)
    return names,location,address

def get_dist_among_pos(key,names,location,address,save_folder):
    dist_mat=[[0 for i in range(50)] for i in range(50)]
    dura_mat=[[0 for i in range(50)] for i in range(50)]
    dist_url='http://restapi.amap.com/v3/direction/walking'
    for i in range(50):
        for j in range(i+1,50):
            if len(address[i]&address[j])==0:
                dist_mat[i][j] = np.inf
                dura_mat[i][j] = np.inf
            else:
                dist_param={
                            'origin':location[i],
                            'destination':location[j],
                            'key':key
                            }
                dist_r=re.get(dist_url,dist_param)
                dist_r.encoding='utf-8'
                dist_r_json=dist_r.json()
                dist_mat[i][j]=dist_r_json["route"]["paths"][0]["distance"]
                dura_mat[i][j]=dist_r_json["route"]["paths"][0]["duration"]
                time.sleep(0.02)

    print(dist_mat)
    for i in range(50):
        for j in range(0,i):
            dist_mat[i][j]=dist_mat[j][i]
            dura_mat[i][j]=dura_mat[j][i]

    dist_mat=np.array(dist_mat)
    dura_mat=np.array(dura_mat)
    dist_df=pd.DataFrame(dist_mat,index=names,columns=names)
    dura_df=pd.DataFrame(dura_mat,index=names,columns=names)
    filename = pd.ExcelWriter(save_folder+'\\dist_dura_data.xlsx')
    dist_df.to_excel(filename,sheet_name="Distance")
    dura_df.to_excel(filename,sheet_name="Duration")

if __name__=='__main__':
    mykey = '70a897d6dd09533575951e02effb151a'
    keyword='公交站'
    save_folder=keyword+'数据'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    stop_names,stop_location,stop_address=search_pos(mykey,keyword,save_folder=save_folder)
    get_dist_among_pos(mykey,stop_names,stop_location,stop_address,save_folder=save_folder)