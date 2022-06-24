import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import lasio as ls
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import scipy

st.title("""MDT Presssure Points analysis  """)

st.header("Upload the  Production  data file here ")
st.markdown(" The file format is  standard Excel File")

data_uploader = st.file_uploader("upload file", type={"csv", "txt",'las'})
if data_uploader is not None:
          data_uploader.seek(0)
          string = data_uploader.read().decode()
          
          log=ls.read(string)
          temp_df1=log.df()
          temp_df1=temp_df1.reset_index()
          temp_df1.columns
          temp_df1.rename(columns = {'DEPT':'DEPTH','SGRC':'GR','TNPL':'NPHI','PEF':'PE','HSI':'CALI'
                              ,'SBD2':'RHOB','PRES2M16IN':'RS','PRES500K48IN':'RT','SROP':'ROP',"SFXE":'FEXP'}, inplace = True)
          temp_df1=temp_df1.dropna()

          temp_df1=temp_df1[['DEPTH','ROP','GR','NPHI','PE','CALI','RHOB','RS','RT','ROP','FEXP','RPM']] 
          data_df=temp_df1.copy()


st.sidebar.header("User input parameter")
step_size=st.sidebar.slider('Interval Analysis Block Size m',0.0,5.0,value=1.0)
limit_cali=st.sidebar.slider('Calipher Limit in  m',0.0,1.4,value=0.05)
limit_gr=st.sidebar.slider('Gamma Ray Limit in  m',0.0,10.5,value=5.1)
limit_d=st.sidebar.slider('Density Limit in  m',0.0,10.5,value=5.1)
limit_p=st.sidebar.slider('Porosity Limit in  m',0.0,60.0,value=10.8)
limit_p=limit_p/100
lim_sim_res=st.sidebar.slider('Similarity  in Shallow & Deep Resistivity  m',0.0,60.0,value=10.8)
st.header("The Input Well Log Data ")
st.dataframe(data_df)
def making_blocks(df2,step_size,block):
    t_df_list=[]
    depth_min=int(np.amin(df2[['DEPTH']].values))
    depth_max=int(np.amax(df2[['DEPTH']].values))+1
    a=depth_min
    df=df2.copy()
    for i in range (int((depth_max-depth_min)/step_size)-1):
        t_df=df[(df['DEPTH']>a) & (df['DEPTH']<=(a+block))]
        t_df_list.append(t_df)
        a=a+step_size
    return t_df_list  
def filter_list_df(d_list,thresh_c,thresh_g,thresh_d,thresh_p,thresh_r):
    cali_list=[]
    for i in range(len(d_list)):
        dev_c=d_list[i]['CALI'].std()
        dev_g=d_list[i]['GR'].std()
        dev_d=d_list[i]['RHOB'].std()
        dev_p=d_list[i]['NPHI'].std()
        dis_r=scipy.spatial.distance.cdist(
                d_list[i]['RS'].values.reshape(-1,len(d_list[i]['RS'].values))
               ,d_list[i]['RT'].values.reshape(-1,len(d_list[i]['RT'].values))
                )
        
        if (dev_c<=thresh_c) & (dev_g<=thresh_g)& (dev_d<=thresh_d) & (dev_p<=thresh_p) & (dis_r<=thresh_r):
            cali_list.append(i)
   
    return cali_list      
list=making_blocks(temp_df1,1,step_size)
filt_list_ind=filter_list_df(list,limit_cali,limit_gr,limit_d,limit_p,lim_sim_res)
 
for i in range(len(filt_list_ind)):
     st.header("The Filtered Data points "+i)
     ind=filt_list_ind[i]
     st.dataframe(list[ind])
 
