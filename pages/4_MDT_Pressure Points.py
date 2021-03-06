import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import lasio as ls
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import scipy
from scipy import spatial

st.title("""Identification of Formation Testing Pressure Points """)

st.header("Upload the  LWD Log Data File here ")
st.markdown(" The file format is  standard LAS File")

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
          std_cali=temp_df1['CALI'].std()
          std_gr=temp_df1['GR'].std()
          std_p=temp_df1['NPHI'].mean()
          std_d=temp_df1['RHOB'].mean()
          mean_r=temp_df1['RT'].mean()
          data_df=temp_df1.copy()


st.sidebar.header("User input parameter")
step_size=st.sidebar.slider('Interval Analysis Block Size m',0.0,5.0,value=1.0)
limit_cali=st.sidebar.slider('Calipher Limit in  m',0.0,100.0,value=38.5)
limit_cali=limit_cali*std_cali/100
limit_gr=st.sidebar.slider('Gamma Ray Limit in  m',0.0,100.0,value=20.4)
limit_gr=limit_gr*std_gr/100
limit_d=st.sidebar.slider('Density Limit in  m',0.0,100.0,value=20.5)
limit_d=limit_d*std_d/100
limit_p=st.sidebar.slider('Porosity Limit in  m',0.0,100.0,value=65.2)
limit_p=limit_p*std_p/100

lim_sim_res=st.sidebar.slider('Similarity  in Shallow & Deep Resistivity  m',0.0,10.0,value=3.5)
lim_sim_res=lim_sim_res*mean_r
st.header("The Input Well Log Data ")
#st.write(data_df,200,100)
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
        dis_r=spatial.distance.cdist(
                d_list[i]['RS'].values.reshape(-1,len(d_list[i]['RS'].values))
               ,d_list[i]['RT'].values.reshape(-1,len(d_list[i]['RT'].values))
                )
        
        if (dev_c<=thresh_c) & (dev_g<=thresh_g)& (dev_d<=thresh_d) & (dev_p<=thresh_p) & (dis_r<=thresh_r):
            cali_list.append(i)
   
    return cali_list      
list=making_blocks(temp_df1,1,step_size)
filt_list_ind=filter_list_df(list,limit_cali,limit_gr,limit_d,limit_p,lim_sim_res)
 
for i in range(len(filt_list_ind)):
     #st.header("The Filtered Data points "+str(i))
     ind=filt_list_ind[i]
     #st.dataframe(list[ind])
 
def dataframe_final_points(orig_list,index_list):
    list_to=[]
    for i in range(len(index_list)):
              val=orig_list[index_list[i]]
              list_to.append(val)
    df_tops=pd.concat(list_to)   
    return df_tops #returns the datfarem combining all the values filtered
df_mdt=dataframe_final_points(list,filt_list_ind).drop_duplicates()
depth_df_mdt=df_mdt['DEPTH'].values
def log_plot(well,df,depth_mdt,depth_mdt_actual, column_depth, column_GR, column_resistivity, 
                 column_NPHI, column_RHOB, min_depth, max_depth, 
                 min_GR=0, max_GR=150, sand_GR_line=60,
                 min_resistivity=0.2, max_resistivity=200, 
                 color_GR='green', color_resistivity='black', 
                 color_RHOB='red', color_NPHI='blue',
                 figsize=(28,22), tight_layout=1, 
                 title_size=35, title_height=1):
   
  import matplotlib.pyplot as plt
  from matplotlib.ticker import AutoMinorLocator  

  fig, ax=plt.subplots(1,3,figsize=(28,22),dpi=55)
  fig.suptitle(well[0]+'  Well Logs with Higlighted Pressure Recording Points ', size=title_size, y=title_height)

  ax[0].minorticks_on()
  ax[0].grid(which='major', linestyle='-', linewidth='1', color='brown')
  ax[0].grid(which='minor', linestyle=':', linewidth='1.5', color='black')

  ax[1].minorticks_on()
  ax[1].grid(which='major', linestyle='-', linewidth='1', color='brown')
  ax[1].grid(which='minor', linestyle=':', linewidth='1.5', color='black')

  ax[2].minorticks_on()
  ax[2].grid(which='major', linestyle='-', linewidth='1', color='brown')
  ax[2].grid(which='minor', linestyle=':', linewidth='1.5', color='black')  

  # First Log Generally as per industrial standard
  ax[0].get_xaxis().set_visible(False)
  ax[0].invert_yaxis()   

  gr=ax[0].twiny()
  gr.set_xlim(min_GR,max_GR)
  gr.set_xlabel('Gamma Ray',color=color_GR)
  gr.set_ylim(max_depth, min_depth)
  gr.spines['top'].set_position(('outward',10))
  gr.tick_params(axis='x',colors=color_GR)
  gr.plot(df[column_GR], df[column_depth], color=color_GR,lw=3.5)  
  gr.plot(df[column_GR], df[column_depth], color=color_GR) 
  gr.minorticks_on()
  gr.xaxis.grid(which='major', linestyle='-', linewidth='1', color='brown')
  gr.xaxis.grid(which='minor', linestyle=':', linewidth='1.5', color='black')
  for i in range(len(depth_mdt)):
        gr.axhline(y=depth_mdt[i],color='chocolate')
  #for i in range(len(depth_mdt_actual)):
  #     gr.axhline(y=depth_mdt_actual[i],color='black')
 

  # Second Log is Deep Resistivity Resistivity
  ax[1].get_xaxis().set_visible(False)
  ax[1].invert_yaxis()   

  resistivity=ax[1].twiny()
  resistivity.set_xlim(min_resistivity,max_resistivity)
  resistivity.set_xlabel('Resistivity',color=color_resistivity)
  resistivity.set_ylim(max_depth, min_depth)
  resistivity.spines['top'].set_position(('outward',10))
  resistivity.tick_params(axis='x',colors=color_resistivity)
  resistivity.semilogx(df[column_resistivity], df[column_depth], color=color_resistivity,lw=3.5)    

  resistivity.minorticks_on()
  resistivity.xaxis.grid(which='major', linestyle='-', linewidth='1', color='brown')
  resistivity.xaxis.grid(which='minor', linestyle=':', linewidth='1.5', color='black')   

  # Third Log path is for  NPHI and RHOB as per standard convention
  ax[2].get_xaxis().set_visible(False)
  ax[2].invert_yaxis()  

  ## NPHI curve 
  nphi=ax[2].twiny()
  nphi.set_xlim(-0.06,0.54)
  nphi.invert_xaxis()
  nphi.set_xlabel('NPHI',color='blue')
  nphi.set_ylim(max_depth, min_depth)
  nphi.spines['top'].set_position(('outward',10))
  nphi.tick_params(axis='x',colors='blue')
  nphi.plot(df[column_NPHI], df[column_depth], color=color_NPHI,lw=3.5)

  nphi.minorticks_on()
  nphi.xaxis.grid(which='major', linestyle='-', linewidth='1', color='brown')
  nphi.xaxis.grid(which='minor', linestyle=':', linewidth='1.5', color='black')     

  ## RHOB curve 
  density=ax[2].twiny()
  density.set_xlim(1.8,2.8)
  density.set_xlabel('RHOB',color='red')
  density.set_ylim(max_depth, min_depth)
  density.spines['top'].set_position(('outward',50))
  density.tick_params(axis='x',colors='red')
  density.plot(df[column_RHOB], df[column_depth], color=color_RHOB,lw=3.5)

 
  x2p, _ = (density.transData + nphi.transData.inverted()).transform(np.c_[df[column_RHOB], df[column_depth]]).T
  nphi.autoscale(False)
  nphi.fill_betweenx(df[column_depth], df[column_NPHI], x2p, color="orange", alpha=0.4, where=(x2p > df[column_NPHI])) # hydrocarbon
  nphi.fill_betweenx(df[column_depth], df[column_NPHI], x2p, color="blue", alpha=0.4, where=(x2p < df[column_NPHI])) # water

  resistivity.minorticks_on()
  resistivity.grid(which='major', linestyle='-', linewidth='1', color='brown')
  resistivity.grid(which='minor', linestyle=':', linewidth='1.5', color='black')

  
  return fig
depth_mdt_actual_7a9=[2740.03,2726.97,2719.99,2718.49,2717.02,2711.53,2697.99,2683.49]
depth_mdt_actual_7a8=[1686.56,1687.5,1690.5,1701,1712]
well_name=['Well_1']
fig1=log_plot(well_name,temp_df1,depth_df_mdt,depth_mdt_actual_7a8, 'DEPTH', 'GR', 'RT', 'NPHI', 'RHOB', 
             min_depth=1650, max_depth=1720, 
             min_GR=0, max_GR=100, sand_GR_line=50,
             max_resistivity=10000,
             figsize=(28,22), title_size=35, title_height=1)
st.text('Well Data with Highlighted MDT Points')
#st.set_option('depreciation.showPyplotGlobalUse',False)
st.pyplot(fig1,width=35)
 
