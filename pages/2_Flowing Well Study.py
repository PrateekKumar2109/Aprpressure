import openpyxl
import numpy as np
import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import os

st.title("""Flowing  Well Study Interpretation Web Application""")
wellname=['Well_1']

st.header("Upload the Deviation data file here ")
st.markdown(" The file format is  MDKB in m,TVDSSin m, Azimuth & Inclination")
data_uploader = st.file_uploader("upload file", type={"csv", "txt"})
if data_uploader is not None:
    data_df = pd.read_csv(data_uploader)
    #data_df['TVDSS']=data_df["TVDKB"]-kb
st.header("The Input Well Deviation Data ")
st.dataframe(data_df)
st.header("Upload the FLGR Survey  data file here")
st.markdown(" The file format is  columns Depth MDKB  in md-ft, pressure & temperature")
data_uploader2 = st.file_uploader("upload file 2", type={"csv", "txt",'xlsx'})
if data_uploader2 is not None:
    
    wb=openpyxl.load_workbook(data_uploader2)
    flw_st_name=wb.sheetnames
    dataframe_list=[]
    for i in range(len(flw_st_name)):
    
        temp_df=pd.read_excel(data_uploader2,sheet_name=flw_st_name[i])
        dataframe_list.append(temp_df)  
st.sidebar.header("User input parameter")
flw_st_nam=np.array(flw_st_name)
num_surveys=st.sidebar.multiselect("Select Survey data for analysis",options=flw_st_nam,default=flw_st_name[0:])
num_figure=len(num_surveys)
activities=['Pressure','Temperature','Both']
choice=st.sidebar.selectbox("Select Parameter", activities)
gas_gradient=st.sidebar.slider('Injection Gas Grad',0.0,0.4,value=0.1)
gas_inj_p=st.sidebar.number_input('Enter the Gas Injection Pressure(GIP) in psi',step=10)
#gas_inj_p=st.sidebar.slider('Gas Injection Pressure',400,1400,value=600)
ang_lim=st.sidebar.slider('Inclination angle Cut',40,90,value=65)
kb=st.sidebar.slider('KB(Kelly Bushing)in m',30.5,45.5,value=36.72)

kb_th=st.sidebar.slider('KB_TH distance in m',8.5,25.5,value=17.9)
#grad_y=np.arange(start=50, stop=500, step=50)#spacing in gradients
grad_y=np.array([0,50,100,150,200])
def slope(x1, y1, x2, y2):#calculates slope on point basis
  s = (y2-y1)/(x2-x1)
  return (s)
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
    names=['TVDSS']
    data=[]
    for j in range(len(names)):
        y=data_df1[names[j]]
        i=x[x>a].index[0]-1
        d=y[i]+((y[i+1]-y[i])*(a-x[i])/(x[i+1]-x[i]))
        data.append(d)
    return data[0] 
def flwing_press_temp_plt(wellnam,df_final_list,y_c,ang_point,gas_grad,gip,choice1,num_fgs):
    df_final=df_final_list[0]
    y_v_line=np.arange(200, (df_final['PRESSURE'].values[0]+100), 100)
    x_v_line=np.arange(200, (df_final['TVDSS'].values[0]+100), 100)
    c=df_final['GL DEPTH TVDSS'].values
    m=[0,0,0,0]
    headings=df_final['VALVES'].values
    
    fig=plt.figure(figsize=(24,20),dpi=90)
    ax = fig.add_subplot(211)

    ax.set_title(wellnam+' FBHP Pressure with Depth Plot ',fontsize=20)
    ax.plot(x_v_line,gas_grad*x_v_line+gip,color='black',lw=1.5)
    ax.plot(ang_point,250,color='red',marker='o',markersize=12)
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
    #ax.legend(loc=1,fontsize='x-large')


#ax.set_xlim(['Aug-18', 'Apr-21'])
    ax.set_ylabel("Pressure in psi",color="brown",fontsize=22,labelpad=10)
    ax.tick_params( axis='y',labelsize=13,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
#ax.set_xticklabels(df_final['PRESSURE'],fontsize=14)
#ax.set_xticklabels(fontsize=14)
    ax.set_xlabel(xlabel="Depth in TVDSS",color="black",fontsize=18)
    ax2=ax.twinx()
    label_wekk=[]
    label_wekk_p=[]
    label_wekk_t=[] 
    
    for p in range(num_fgs):
        label_wekk.append(flw_st_name[p]+" grad.  ")
        label_wekk_p.append(flw_st_name[p]+' Pressure')
        label_wekk_t.append(flw_st_name[p]+' Temperature')
    
    if choice1=='Pressure':
        for k in range(num_fgs):
           ax.plot(df_final_list[k]['TVDSS'],df_final_list[k]['PRESSURE'],marker="v",lw=2.5,label=label_wekk_p[k],markersize=9)
           sl=slope(df_final_list[k]['TVDSS'].values[-1], df_final_list[k]['PRESSURE'].values[-1]
                 , df_final_list[k]['TVDSS'].values[0],df_final_list[k]['PRESSURE'].values[0])
           sl= str(round(sl,2))+' psi/m'
           ax.text((df_final_list[k]['TVDSS'].values[-1]-250),(int(df_final['PRESSURE'].values[0])+int(grad_y[k])),s=(label_wekk[k]+sl),fontsize='x-large')
           #ax.plot(df_final_list[k]['TVDSS'].values,df_final_list[k]['PRESSURE'],marker="v",lw=2.5,label=label_wekk_p[k],markersize=9)
    elif choice1=='Temperature':   
        for l in range(num_fgs):
           ax2.plot(df_final_list[l]['TVDSS'],df_final_list[l]['TEMPERATURE'],marker="o",lw=2.5,label=label_wekk_t[l])
    
    elif choice1=='Both':   
        for k in range(num_fgs):
           ax.plot(df_final_list[k]['TVDSS'],df_final_list[k]['PRESSURE'],marker="v",lw=2.5,label=label_wekk_p[k],markersize=9)
           sl=slope(df_final_list[k]['TVDSS'].values[-1], df_final_list[k]['PRESSURE'].values[-1]
                 , df_final_list[k]['TVDSS'].values[0],df_final_list[k]['PRESSURE'].values[0])
           sl=str(round(sl,2))+' psi/m'
           ax.text((df_final_list[k]['TVDSS'].values[-1]-250),(int(df_final['PRESSURE'].values[0])+int(grad_y[k])),s=(label_wekk[k]+sl),fontsize='x-large')
           ax2.plot(df_final_list[k]['TVDSS'],df_final_list[k]['TEMPERATURE'],marker="o",lw=2.5,label=label_wekk_t[k])
   
    
    ax2.set_ylim([(df_final['TEMPERATURE'].values[-1]-10),(df_final['TEMPERATURE'].values[0]+10)])
    ax2.set_xlim([0,(df_final['TVDSS'].values[0]+100)])
#ax2.set_ylim([-100,(df_final['TVDSS'].values[0]+100)])
#plt.gca().invert_yaxis()
#ax2.invert_yaxis()
    ax.tick_params(axis='x',which='minor',direction='out',bottom=True,length=5)
    ax.legend(loc='upper right', fontsize='x-large',bbox_to_anchor=(0.15, 0.99))
    ax2.legend(loc='upper right', fontsize='x-large',bbox_to_anchor=(0.3, 0.99))
    ax2.tick_params( axis='y',labelsize=14,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
    ax2.set_ylabel(ylabel="Temperature ",color="blue",fontsize=18)
#ax2.set_xticklabels(df_final['TEMPERATURE'],fontsize=14)
#ax2.set_xticklabels(fontsize=14)
    ax.xaxis.grid(color='black', linestyle='--', linewidth=0.5)
    ax.yaxis.grid(color='black', linestyle='--', linewidth=0.5)
#plt.gca().invert_yaxis()
    #plt.show()
    return fig
df_final_list=[]
for j in range(num_figure):
    
    df_final_temp=dataframe_tvd_converter(data_df,dataframe_list[j],kb_th)
    df_final_list.append(df_final_temp)
    st.header("The Input Pressure & Temp. Survey  Data")
    st.dataframe(df_final_temp) 
st.text('Pressure & Temperature Plot')
wellnam='HSD-5'
y_c=[300,300,300,300]
point=depth_finder(data_df,ang_lim)

fig2=flwing_press_temp_plt(wellnam,df_final_list,y_c,point,gas_gradient,gas_inj_p,choice,num_figure)

st.pyplot(fig2,width=25)                             

