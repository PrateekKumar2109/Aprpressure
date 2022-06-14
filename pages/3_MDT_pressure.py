import openpyxl
import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
#from sklearn import datasets
#from sklearn.metrics import r2_score
import os
st.title("""MDT Pressure Analysis""")
wellname=['Well_1']
k=0
st.sidebar.header("User input parameter")

kb=st.sidebar.slider('KB(Kelly Bushing)in m',30.5,45.5,value=36.72)


gas_gr=st.sidebar.slider('Gas gradient cut off',0.0,0.7,value=0.5)
water_gr=st.sidebar.slider('Water gradient cut off',0.0,1.8,value=1.4)
st.header("Upload the MDT Pressure data file here")
st.markdown(" The file format is  columns Depth MDKB  in m,Depth TVDKB  in m pressure & temperature")
data_uploader2 = st.file_uploader("upload file 2", type={"csv", "txt",'xlsx'})
if data_uploader2 is not None:
    data_df2 = pd.read_excel(data_uploader2)
    data_df2.dropna(inplace=True)
st.header("The Input Pressure & Temp. MDT Non-Zero  Data")
st.dataframe(data_df2)  
def slope(x1, y1, x2, y2):#calculates slope on point basis
  s = (y2-y1)/(x2-x1)
  return 1/s
df_final=data_df2.copy()
df_final['TVDSS']=df_final['TVD']-kb
def gradient_function(press,tvd_depth): #this function makes a list of gradients of each point
    for i in range(len(press)-1):
        grad=slope(press[i],tvd_depth[i],press[i+1],tvd_depth[i+1])
        gradient.append(grad)
    gradient.append(0) # we add zero to match the length for dataframe
    #gradient.append(0) 
    press_grad=gradient.copy()
    return press_grad

gradient=[]
pressure_grad=gradient_function(df_final['PRESSURE'].values, df_final['TVDSS'].values)
df_final['Pressure Gradient']=pressure_grad
def fluid_type(gas_gra,water_gra,dataframe_df):
    grad_arr=dataframe_df['Pressure Gradient'].values
    depth_arr=dataframe_df['TVDSS'].values
    for j in range(len(dataframe_df['PRESSURE'].values)):
               
           if grad_arr[j]>water_gra:
                type.append('water')
                
           elif grad_arr[j]<gas_gra :
                
                type.append('gas')
           else:
                type.append('oil')   
    type_file=np.array(type)
    return type_file

type=[]
df_final_d=df_final.copy()
df_final['Fluid type']=fluid_type(gas_gr,water_gr,df_final)

def pressure_plot_down(well_name,dataframe):
    colors = {'oil':'green', 'gas':'red', 'water':'blue'}
    fig=plt.figure(figsize=(4.6,4.1),dpi=60)
    plt.plot(dataframe['PRESSURE'],dataframe['TVDSS'],color='black',lw=1,label='Pressure')
    #plt.scatter(df_final['PRESSURE'],df_final['TVDSS'],marker='o',c=df_final['Fluid type'].map(colors))
    groups = df_final.groupby('Fluid type')
    for name, group in groups:
        plt.scatter(group.PRESSURE, group.TVDSS, label=name,color=colors[name],marker='o',s=18)
    plt.ylim((dataframe['TVDSS'].values[-1]-100),(dataframe['TVDSS'].values[0]+100))
    plt.gca().invert_yaxis()
    plt.ylabel("Depth in TVDSS",color="black",fontsize=9)
    #label_o=' Oil Gradient is '+str(round(a,2))+' psi/m'
    plt.xlabel("Pressure in psi",color="black",fontsize=9)
    plt.tick_params(axis='both',labelsize=6)
    plt.title(well_name+'  Interactive Interpretation  ',fontsize=11)
    plt.grid(axis='both')
    #plt.rcParams['xtick.top']=plt.rcParams['xtick.labeltop']=True
    plt.rcParams['xtick.bottom']=plt.rcParams['xtick.labelbottom']=True
    #plt.text(1000,2000,(df_final['PRESSURE']+df_final['TVDSS'].values[0]))
    #plt.plot(x_line, a*x_line+b,color='green',linestyle='dotted')

    #label = ' Pressure  is '+str(round(xs,2))+' psi'
      
    plt.legend(fontsize=7)
    return fig

st.text('Pressure Plot with gradients')
fig1=pressure_plot_down(wellname[k],df_final)
st.pyplot(fig1,width=30)  
