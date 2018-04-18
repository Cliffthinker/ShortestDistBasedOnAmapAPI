import requests as re
import time
import numpy as np
import pandas as pd

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
#    loc_str=r_json["pois"][i]["location"]
#    loc=tuple(map(float,loc_str.split(',')))
#    cam_location.append(loc)
    cam_location.append(r_json["pois"][i]["location"])
print(cam_names)
for each in cam_location:
    print(each)

dist_mat=[[0 for i in range(30)] for i in range(30)]
dura_mat=[[0 for i in range(30)] for i in range(30)]
dist_url='http://restapi.amap.com/v3/direction/walking'

for i in range(30):
    for j in range(i+1,30):
        dist_param={
                    'origin':cam_location[i],
                    'destination':cam_location[j],
                    'key':mykey
                    }
        dist_r=re.get(dist_url,dist_param)
        dist_r.encoding='utf-8'
        dist_r_json=dist_r.json()

        dist_mat[i][j]=dist_r_json["route"]["paths"][0]["distance"]
        dura_mat[i][j]=dist_r_json["route"]["paths"][0]["duration"]
        time.sleep(0.02)
print(dist_mat)

for i in range(30):
    for j in range(0,i):
        dist_mat[i][j]=dist_mat[j][i]
        dura_mat[i][j]=dura_mat[j][i]

dist_mat=np.array(dist_mat)
dura_mat=np.array(dura_mat)
dist_df=pd.DataFrame(dist_mat,index=cam_names,columns=cam_names)
dura_df=pd.DataFrame(dura_mat,index=cam_names,columns=cam_names)
filename = pd.ExcelWriter('distance_duration_data.xlsx')
dist_df.to_excel(filename,sheet_name="Distance")
dura_df.to_excel(filename,sheet_name="Duration")