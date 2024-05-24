import streamlit as st
import pandas as pd 
from scripts.indicators import *
from scripts.strategy import *
from scripts.charts import *
import plotly.graph_objects as go


st.set_page_config(
    page_title="Trading App",
    page_icon="img/icon.png",  # You can use emojis or the path to an image file
    layout="wide"
)

hist = pd.read_csv('notebooks/BTC-EUR.csv')

tabs = st.tabs(["Dashboard","Strategy Optimizer","Model Studio","Recommandations"])

with tabs[0]:
    st.header('Dashboard')

    st.subheader('Your Trades')

    short = st.slider('Short Window', min_value=5, max_value=20, value=7)
    long = st.slider('Long Window', min_value=20, max_value=50, value=27)
    
    df = calculate_sma(hist,short_window=short, long_window=long)
    df = generate_sma_signals(df)
    df, trades = apply_strategy(df)
    trades = pd.DataFrame(trades)
    col1,col2 = st.columns(2)
    with col1:
        st.table(trades)
        performance_frame = performance_df(trades)
    with col2 :
        st.table(performance_frame)

    
    col1,col2 = st.columns(2)
    with col1:
        fig = px.line(df,x='Date',y=['Close','Short_SMA','Long_SMA'])
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        fig = showtrades(hist,trades,hist['Close'], annot=True)
        st.plotly_chart(fig,use_container_width=True)


   

with tabs[1]:
    st.header('Strategy Optimizer')

with tabs[2]:
    st.header('Model Studio')

with tabs[3]:
    st.header('Recommandations')   