#pip install matplotlib
import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
#from sklearn import datasets
#from sklearn.metrics import r2_score
import os
st.title("""Static Well Study Interpretation Web Application""")
wellname=['Well_1']
st.sidebar.header("User input parameter")

kb=st.sidebar.slider('KB(Kelly Bushing)in m',30.5,45.5,value=36.72)

kbth=st.sidebar.slider('KB_TH distance in m',8.5,25.5,value=17.32)
de=st.sidebar.slider(' Oil top Dotted line',0,20,value=7)
t=st.sidebar.slider(' Oil bottom Dotted line',0,15,value=5)
#gde=st.sidebar.slider('Upper Dotted line',0,15,value=5)
gas_gr=st.sidebar.slider('Gas gradient cut off',0.0,0.7,value=0.5)
water_gr=st.sidebar.slider('Water gradient cut off',0.0,1.8,value=1.4)

k=0

#kb=36.72
#kbth=17.32
data_uploader = st.file_uploader("upload file", type={"csv", "txt"})
if data_uploader is not None:
    data_df = pd.read_csv(data_uploader)
    #data_df['TVDSS']=data_df["TVDKB"]-kb
st.header("The Loaded Deviation Data ")
st.dataframe(data_df)

data_uploader2 = st.file_uploader("upload file 2", type={"csv", "txt"})
if data_uploader2 is not None:
    data_df2 = pd.read_csv(data_uploader2)
    
st.header("The Loaded Pressure Data Expro format")
st.dataframe(data_df2)
df_convert=data_df2.copy()
df_convert=df_convert[['DEPTH', 'PRESSURE', 'TEMPERATURE']]
df_final=df_convert.copy()
df=data_df.copy()
a=df_convert['DEPTH'].dropna(axis=0)*(0.3048)+kbth
a=a.values
df_final['MDKB']=a
x=df['MDKB']
y=df['TVDSS']
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

if len(tvd)==len(df_convert['DEPTH'].values):
    
    df_final['TVDSS']=tvd#adding TVD column in dataframe#
    
else:
    tvd.append(0)
    df_final['TVDSS']=tvd


#df_final['TVDSS']=tvd#adding TVD column in dataframe#

#df_final.reset_index(inplace=True)
#df_final.reset_index(inplace=True)
df_final=df_final[['DEPTH','MDKB','TVDSS', 'PRESSURE', 'TEMPERATURE']]

def slope(x1, y1, x2, y2):#calculates slope on point basis
  s = (y2-y1)/(x2-x1)
  return 1/s

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
df_final['Fluid type']=fluid_type(gas_gr,water_gr,df_final) # here we type the points on the basis of their gradient value
x_np=df_final['PRESSURE'].values[t:de]#selecting for below gradient
x_np=np.asfarray(x_np)
x_np
y_np=df_final['TVDSS'].values[t:de]
y_np=np.asfarray(y_np)
a, b = np.polyfit(x_np, y_np, 1)
x_line=np.arange(200, df_final['PRESSURE'].values[0], 100)

x_gp=df_final['PRESSURE'].values[:]#selecting for gas gradient
x_np=np.asfarray(x_np)
x_np
y_np=df_final['TVDSS'].values[t:de]
y_np=np.asfarray(y_np)
a, b = np.polyfit(x_np, y_np, 1)
x_line=np.arange(200, df_final['PRESSURE'].values[0], 100)

xs=int(df_final['PRESSURE'].values[0])
ys=int(df_final['TVDSS'].values[0])

x_v_line=np.arange(200, df_final['PRESSURE'].values[0], 100)
c=[1750,1610,1500,1300]
m=[0,0,0,0]
headings=['CV','MMG','MMG2','MMG3']
x_c=[800,800,800,800]

def pressure_temp_plot(well_name,dataframe):
    #fig=plt.figure(figsize=(4.2,5.2),dpi=45)
    fig=plt.figure(figsize=(10,20),dpi=40)
    ax = fig.add_subplot(211)

    ax.set_title(well_name+' SBHP Pressure with Depth Plot ',fontsize=20)
    ax.plot(dataframe['PRESSURE'],dataframe['TVDSS'],color='brown',marker="o",lw=2.5,label='Pressure')
    #ax.plot(x_v_line,m[0]*x_v_line+c[0],color='black',lw=1.5)
    #ax.plot(x_v_line,m[1]*x_v_line+c[1],color='black',lw=1.5)
    #ax.plot(x_v_line,m[2]*x_v_line+c[2],color='black',lw=1.5)
    #ax.plot(x_v_line,m[3]*x_v_line+c[3],color='black',lw=1.5)
    #ax.text(x_c[0],c[0],s=headings[0],fontsize='large')
    #ax.text(x_c[1],c[1],s=headings[1],fontsize='large')
    #ax.text(x_c[2],c[2],s=headings[2],fontsize='large')
    #ax.text(x_c[3],c[3],s=headings[3],fontsize='large')
    ax.plot()
    
    ax.set_xlim([200,(dataframe['PRESSURE'].values[0]+200)])
    ax.set_ylim([(dataframe['TVDSS'].values[0]+100),-100])
    ax.set_ylim([-100,(dataframe['TVDSS'].values[0]+100)])
    plt.gca().invert_yaxis()
    ax.invert_yaxis()
    ax.legend(loc=1,fontsize='x-large')
    ax.set_xlabel("Pressure in psi",color="brown",fontsize=22,labelpad=10)
    ax.tick_params( axis='y',labelsize=13,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
    ax.set_xticklabels(dataframe['PRESSURE'],fontsize=14)
    #ax.set_xticklabels(fontsize=14)
    ax.set_ylabel("Depth in TVDSS",color="black",fontsize=18)
    ax2=ax.twiny()
    ax2.plot(dataframe['TEMPERATURE'],dataframe['TVDSS'],color="blue",marker="o",lw=2.5,label='Temperature')
    ax2.set_xlim([50,(dataframe['TEMPERATURE'].values[0]+50)])
    ax2.set_ylim([(dataframe['TVDSS'].values[0]+100),-100])
    ax2.set_ylim([-100,(dataframe['TVDSS'].values[0]+100)])
    plt.gca().invert_yaxis()
    ax2.invert_yaxis()
    ax.tick_params(axis='x',which='minor',direction='out',bottom=True,length=5)
    ax2.legend(loc='upper right', fontsize='x-large',bbox_to_anchor=(0.99, 0.94))
    ax2.tick_params( axis='y',labelsize=14,direction='out', length=6, width=2, colors='black',
              grid_color='r', grid_alpha=0.5)
    ax2.set_xlabel("Temperature ",color="blue",fontsize=18)
    ax2.set_xticklabels(dataframe['TEMPERATURE'],fontsize=14)
    #ax2.set_xticklabels(fontsize=14)
    ax.xaxis.grid(color='black', linestyle='--', linewidth=0.5)
    ax.yaxis.grid(color='black', linestyle='--', linewidth=0.5)
    plt.gca().invert_yaxis()
    plt.show()
    return fig

#

def pressure_plot_down(well_name,dataframe):
    colors = {'oil':'green', 'gas':'red', 'water':'blue'}
    fig=plt.figure(figsize=(2.2,3),dpi=30)
    plt.plot(dataframe['PRESSURE'],dataframe['TVDSS'],color='black',lw=1,label='Pressure')
    #plt.scatter(df_final['PRESSURE'],df_final['TVDSS'],marker='o',c=df_final['Fluid type'].map(colors))
    groups = df_final.groupby('Fluid type')
    for name, group in groups:
        plt.scatter(group.PRESSURE, group.TVDSS, label=name,color=colors[name],marker='o',s=20)
    plt.ylim(-100,(dataframe['TVDSS'].values[0]+100))
    plt.gca().invert_yaxis()
    plt.ylabel("Depth in TVDSS",color="black",fontsize=8)
    label_o=' Oil Gradient is '+str(round(a,2))
    plt.xlabel("Pressure in psi",color="brown",fontsize=8)
    plt.tick_params(axis='both',labelsize=4)
    plt.title(well_name+' Interpretation Plot ',fontsize=9)
    plt.grid(axis='both')
    plt.rcParams['xtick.top']=plt.rcParams['xtick.labeltop']=True
    plt.rcParams['xtick.bottom']=plt.rcParams['xtick.labelbottom']=True
    #plt.text(1000,2000,(df_final['PRESSURE']+df_final['TVDSS'].values[0]))
    plt.plot(x_line, a*x_line+b,color='blue',linestyle='dotted')

    label = xs,ys
    
    plt.annotate(label, # this is the text
                 (xs,ys), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(-100,0), # distance from text to points (x,y)
                 ha='left',fontsize=6) # horizontal alignment can be left, right or center
    plt.annotate(label_o, # this is the text
                 (xs-400,ys-400), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(-100,0), # distance from text to points (x,y)
                 ha='left',fontsize=6)
    
    plt.legend(fontsize=6)
    return fig

st.text('Pressure & Temperature Plot')
fig2=pressure_temp_plot(wellname[k],df_final)
st.pyplot(fig2,width=20)

st.text('Pressure Plot with gradients')
fig1=pressure_plot_down(wellname[k],df_final)
st.pyplot(fig1,width=20)


