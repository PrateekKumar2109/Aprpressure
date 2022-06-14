import openpyxl
import numpy as np
import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import os

st.title("""Flowing  Well Study Interpretation Web Application""")
wellname=['Well_1']
st.sidebar.header("User input parameter")

kb=st.sidebar.slider('KB(Kelly Bushing)in m',30.5,45.5,value=36.72)
gas_gradient=st.sidebar.slider('Injection Gas Grad',0.0,0.4,value=0.1)
gas_inj_p=st.sidebar.slider('Gas Injection Pressure',200,1200,value=400)
num_figure=st.sidebar.slider('Number of Surveys',1,7,value=2)
activities=['Pressure','Temperature','Both']
choice=st.sidebar.selectbox("Select Activity", activities)

num_figure=num_figure-1
kb_th=st.sidebar.slider('KB_TH distance in m',8.5,25.5,value=17.9)
ang_lim=st.sidebar.slider('Maximum angle for tool',40,90,value=65)
st.header("Upload the Deviation data file here ")
st.markdown(" The file format is  MDKB in m,TVDSSin m, Azimuth & Inclination")
data_uploader = st.file_uploader("upload file", type={"csv", "txt"})
if data_uploader is not None:
    data_df = pd.read_csv(data_uploader)
    #data_df['TVDSS']=data_df["TVDKB"]-kb
st.header("The Input Deviation Data ")
st.dataframe(data_df)
st.header("Upload the Flowing  data file here")
st.markdown(" The file format is  columns Depth MDKB  in md-ft, pressure & temperature")
data_uploader2 = st.file_uploader("upload file 2", type={"csv", "txt",'xlsx'})
if data_uploader2 is not None:
    
    wb=openpyxl.load_workbook(data_uploader2)
    flw_st_name=wb.sheetnames
    dataframe_list=[]
    for i in range(len(flw_st_name)):
    
        temp_df=pd.read_excel(data_uploader2,sheet_name=flw_st_name[i])
        dataframe_list.append(temp_df)  
def dataframe_tvd_converter(dev_data_df,data_to_convert,kbth):
    x_1=dev_data_df['MDKB']
    y_1=dev_data_df['TVDSS']
    data_to_convert=data_to_convert[['DEPTH', 'PRESSURE', 'TEMPERATURE','VALVES', 'GL DEPTH TVDSS']]
    data_new=data_to_convert.copy()
    a=data_to_convert['DEPTH'].dropna(axis=0)*(0.3048)+kbth
    a=a.values
    data_new['MDKB']=a
    tvd_d=[]
    def tvd_converter(a,x,y):
  
       i=x[x>a].index[0]-1  
       d=y[i]+((y[i+1]-y[i])*(a-x[i])/(x[i+1]-x[i]))
       tvd_d.append(d)
       return tvd_d

    tvd=[]
    for i in range(len(a)):
       if a[i]>kbth:
          tvd_d1=tvd_converter(a[i],x_1,y_1)
          tvd.append(tvd_d1)
    
       else:
          tvd.append(0)


    tvd=tvd[0]
    if len(tvd)==len(data_to_convert['DEPTH'].values):
    
       data_new['TVDSS']=tvd#adding TVD column in dataframe#
    
    else:
       tvd.append(0)
       data_new['TVDSS']=tvd
    return data_new
                            
def depth_finder(data_df1,inc_ang):
    x=data_df1['Inc']
    a=inc_ang
    names=['Azimuth', 'TVDSS']
    data=[]
    for j in range(len(names)):
        y=df[names[j]]
        i=x[x>a].index[0]-1
        d=y[i]+((y[i+1]-y[i])*(a-x[i])/(x[i+1]-x[i]))
        data.append(d)
    
def flwing_press_temp_plt(wellnam,df_final_list,y_c,ang_point,gas_grad,gip,choice1,num_fgs):
    df_final=df_final_list[0]
    y_v_line=np.arange(200, (df_final['PRESSURE'].values[0]+100), 100)
    x_v_line=np.arange(200, (df_final['TVDSS'].values[0]+100), 100)
    c=df_final['GL DEPTH TVDSS'].values
    m=[0,0,0,0]
    headings=df_final['VALVES'].values
    
    fig=plt.figure(figsize=(12,16),dpi=70)
    ax = fig.add_subplot(211)

    ax.set_title(wellnam+' FBHP Pressure with Depth Plot ',fontsize=20)
    ax.plot(x_v_line,gas_grad*x_v_line+gip,color='black',lw=1.5)
    ax.plot(ang_point,0,color='red')
    ax.plot(m[0]*y_v_line+c[0],y_v_line,color='black',lw=1.5)
    ax.plot(m[1]*y_v_line+c[1],y_v_line,color='black',lw=1.5)
    ax.plot(m[2]*y_v_line+c[2],y_v_line,color='black',lw=1.5)
    ax.plot(m[3]*y_v_line+c[3],y_v_line,color='black',lw=1.5)
    ax.text(c[0],y_c[0],s=headings[0],fontsize='x-large')
    ax.text(c[1],y_c[1],s=headings[1],fontsize='x-large')
    ax.text(c[2],y_c[2],s=headings[2],fontsize='x-large')
    ax.text(c[3],y_c[3],s=headings[3],fontsize='x-large')
    #ax.plot()
#ax.plot(data_plot['Date'],data_plot['Qo, bopd'],color='green',marker='o',lw=2.5,label='Oil Rate')
    ax.set_ylim([200,(df_final['PRESSURE'].values[0]+200)])
    ax.set_xlim([0,(df_final['TVDSS'].values[0]+100)])
#ax.set_ylim([-100,(df_final['TVDSS'].values[0]+100)])
#plt.gca().invert_yaxis()
#ax.invert_yaxis()
    ax.legend(loc=1,fontsize='x-large')


#ax.set_xlim(['Aug-18', 'Apr-21'])
    ax.set_ylabel("Pressure in psi",color="brown",fontsize=22,labelpad=10)
    ax.tick_params( axis='y',labelsize=13,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
#ax.set_xticklabels(df_final['PRESSURE'],fontsize=14)
#ax.set_xticklabels(fontsize=14)
    ax.set_xlabel("Depth in TVDSS",color="black",fontsize=18)
    ax2=ax.twinx()
    label_wekk_p=[]
    label_wekk_t=[] 
    
    for p in range(num_fgs):
        label_wekk_p.append(flw_st_name[p]+' Pressure')
        label_wekk_t.append(flw_st_name[p]+' Temperature')
    
    if choice1=='Pressure':
        for k in range(num_fgs):
           ax.plot(df_final_list[k]['TVDSS'],df_final_list[k]['PRESSURE'],marker="o",lw=2.5,label=label_wekk_p[k])
    
    elif choice1=='Temperature':   
        for l in range(num_fgs):
           ax.plot(df_final_list[l]['TVDSS'],df_final_list[l]['TEMPERATURE'],marker="o",lw=2.5,label=label_wekk_t[l])
    
    elif choice1=='Both':   
        for k in range(num_fgs):
           ax.plot(df_final_list[k]['TVDSS'],df_final_list[k]['PRESSURE'],marker="o",lw=2.5,label=label_wekk_p[k])
        for l in range(num_fgs):
           ax.plot(df_final_list[l]['TVDSS'],df_final_list[l]['TEMPERATURE'],marker="o",lw=2.5,label=label_wekk_t[l])
   
    
    ax2.set_ylim([50,(df_final['TEMPERATURE'].values[0]+50)])
    ax2.set_xlim([0,(df_final['TVDSS'].values[0]+100)])
#ax2.set_ylim([-100,(df_final['TVDSS'].values[0]+100)])
#plt.gca().invert_yaxis()
#ax2.invert_yaxis()
    ax.tick_params(axis='x',which='minor',direction='out',bottom=True,length=5)
    ax2.legend(loc='upper right', fontsize='x-large',bbox_to_anchor=(0.99, 0.94))
    ax2.tick_params( axis='y',labelsize=14,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
    ax2.set_xlabel("Temperature ",color="blue",fontsize=18)
#ax2.set_xticklabels(df_final['TEMPERATURE'],fontsize=14)
#ax2.set_xticklabels(fontsize=14)
    ax.xaxis.grid(color='black', linestyle='--', linewidth=0.5)
    ax.yaxis.grid(color='black', linestyle='--', linewidth=0.5)
#plt.gca().invert_yaxis()
    #plt.show()
    return fig
for j in range(num_fgs):
    
    df_final=dataframe_tvd_converter(data_df,dataframe_list[j],kb_th)
 
    st.header("The Input Pressure & Temp. Survey  Data")
    st.dataframe(df_final) 
st.text('Pressure & Temperature Plot')
wellnam='HSD-5'
y_c=[300,300,300,300]
fig2=flwing_press_temp_plt(wellnam,dataframe_list,y_c,point,gas_gradient,gas_inj_p,choice,num_figure)

st.pyplot(fig2,width=20)                             

