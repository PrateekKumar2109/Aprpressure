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

kb_th=st.sidebar.slider('KB_TH distance in m',8.5,25.5,value=17.9)

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
    x=dev_data_df['MDKB']
    y=dev_data_df['TVDSS']
    data_to_convert=data_to_convert[['DEPTH', 'PRESSURE', 'TEMPERATURE','VALVES', 'GL DEPTH TVDSS']]
    data_new=data_to_convert.copy()
    a=data_to_convert['DEPTH'].dropna(axis=0)*(0.3048)+kbth
    a=a.values
    data_new['MDKB']=a
    tvd_d=[]
    def tvd_converter(a):
  
       i=x[x>a].index[0]-1  
       d=y[i]+((y[i+1]-y[i])*(a-x[i])/(x[i+1]-x[i]))
       tvd_d.append(d)
       return tvd_d

    tvd=[]
    for i in range(len(a)):
       if a[i]>kbth:
          tvd_d1=tvd_converter(a[i])
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
 df_final=dataframe_tvd_converter(df,dataframe_list[0],kb_th)
 
 st.header("The Input Pressure & Temp. Survey  Data")
 st.dataframe(df_final)                             
 def flwing_press_temp_plt(wellnam,df_final,y_c):
    y_v_line=np.arange(200, (df_final['PRESSURE'].values[0]+100), 100)
    c=df_final['GL DEPTH TVDSS'].values
    m=[0,0,0,0]
    headings=df_final['VALVES'].values
    
    fig=plt.figure(figsize=(12,16),dpi=70)
    ax = fig.add_subplot(211)

    ax.set_title(wellnam+' FBHP Pressure with Depth Plot ',fontsize=20)
    ax.plot(df_final['TVDSS'],df_final['PRESSURE'],color='brown',marker="o",lw=2.5,label='Pressure')
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
    ax2.plot(df_final['TVDSS'],df_final['TEMPERATURE'],color="blue",marker="o",lw=2.5,label='Temperature')
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
st.text('Pressure & Temperature Plot')
wellnam='HSD-5'
y_c=[600,600,600,600]
fig2=flwing_press_temp_plt(wellnam,df_final,y_c)

st.pyplot(fig2,width=20)                             

