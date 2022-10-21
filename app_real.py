import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#the constant
path='test_0.010.csv'


@st.cache(allow_output_mutation=False)
def get_dataset(path):
    df=pd.read_csv(path)
    df.drop('Unnamed: 0',axis=1,inplace=True)
    return df

def count_rows(rows):
    return len(rows)

def get_unique_value(df,a):
    return np.sort(df[a].unique())

def select_according_time(df,day,hour,minute=None):
    if minute is not None:
        df=df[(df['hour']==hour)&(df['dom']==day)&(df['minute']==minute)]
    if minute is None:
        df=df[(df['hour']==hour)&(df['dom']==day)]
    return df

def get_limit_area_df(df,lat,lon):
    df=df[(df['latitude'].round(1)==lat)&(df['longitude'].round(1)==lon)]
    return df

#change a little from the notebook
def get_seaborn_image(df,a,b):
    fig,ax=plt.subplots()
    lis=df.groupby([a,b]).apply(count_rows)
    lis=lis.reset_index()
    lis=lis.pivot(a,b,0)
    sns.heatmap(lis)
    plt.title(f'the seaborn between {a} and {b}',fontsize=22)
    st.pyplot(fig)


def get_seaborn_map_plus(df,n):
    dff=df[['longitude','latitude']].round(n)
    get_seaborn_image(dff,'longitude','latitude')

def get_streamlit_map_frame(df):
    df=pd.DataFrame({'lat':df['latitude'],'lon':df['longitude']})
    return df


df=get_dataset(path)


#the font end
sp1,sp2,sp3=st.columns(3)
with sp2:
    st.title('WELCOME')



select1=st.sidebar.selectbox('Are you interested in the dataset?',('No','head','tail','describe'))
if select1=='head':
    rows=st.slider('choose rows',0,20,5)
    st.write(df.head(rows))
if select1=='tail':
    rows=st.slider('choose rows',0,20,5)
    st.write(df.tail(rows))
if select1=='describe':
    st.write(df.describe())

select2=st.sidebar.selectbox('Are you interested in the traffic in map every seconds?',('No','Yes'))
if select2=='Yes':
    day=st.select_slider('select the day',get_unique_value(df,'dom'))
    hour=st.select_slider('select the hour',get_unique_value(df,'hour'))
    minute=st.select_slider('select the minute',get_unique_value(df,'minute'))
    data=select_according_time(df,day,hour,minute)
    st.write('if you think the pointa are small, that is normal. this is a sample after all')
    st.map(get_streamlit_map_frame(data))

select3=st.sidebar.selectbox('Are you interested in the seaboen',('No','by time','by area'))
if select3=='by time':
    c1,c2,c3=st.columns(3)
    with c1:
        ck1=st.checkbox('day')
    with c2:
        ck2=st.checkbox('hour')
    with c3:
        ck3=st.checkbox('minute')
    
    if ck1 and ck2 and not ck3:
        a='dom'
        b='hour'
        get_seaborn_image(df,a,b)
    if ck2 and ck3 and not ck1:
        a='hour'
        b='minute'
        get_seaborn_image(df,a,b)
    if ck1 and ck3 and not ck2:
        a='dom'
        b='minute'
        st.write('yesh it is a possible arrangement' )
        st.write("what are you studying at?" )
        get_seaborn_image(df,a,b)
    if ck1 and ck2 and ck3:
        st.error('You can only choose two of them to make a heatmap you know')
    if not ck1 and not ck2 and not ck3:
        st.error('Please click the two elements you are interested')
if select3=='by area':
    n=st.slider('choose the number of values after digit',0,3,1)
    get_seaborn_map_plus(df,n)
   
if select1=='No' and select2=='No' and select3=='No':
    st.write('Sorry None of these functions interest you. Maybe you will be interested [link](https://jinjinb-datacamp-project-8cdse1.streamlitapp.com)')
    expander=st.expander('See more about source code')
    expander.write('Click [Here](https://github.com/wuqianma2024/Project_DataCamp) to see the source code of the page as overall data analysis in github. ')
    expander.write('Click [Here](https://colab.research.google.com/drive/1mtRuIW1jsJBTXSFqJ-3vErGtN9joWntf) to see the colab notebook to build the function as basic analysis of data')
    expander.write('Click[Here](https://github.com/JinJinB/Datacamp) to see the source code of the page as choosing point from a map and see the time spentin github')
    expander.write('Click [Here](https://colab.research.google.com/drive/1Ifsi1afhilcqEsdL1BryThae2PgFB_je?usp=sharing) for the colab notebook to build this function as choosing points and see the shortest way')

    expander2=st.expander('README: Documents for the app')
    expander2.write('Click the [document](https://efrei365net-my.sharepoint.com/:w:/g/personal/jiaen_liu_efrei_net/EUygwC5hy5FMhWVCGU_0nFYBEW3mEXiyzx1m6tiLtVzT6w?e=NDWfsA) to see the report')

    mem=st.sidebar.expander('Team members of DE1:')
    mem.write('''Team - DE1: 
    
            :sunglass:
            LIU Jiaen 
            MA Wuqian
            BAE Jin-Young 
            ''')







    










    



