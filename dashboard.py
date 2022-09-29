import pandas as pd
import requests
import datetime
import streamlit as st
from main import get_market_data
import plotly.graph_objects as go

st.markdown(''' # **FTX Price App**
A simple cryptocurrency price app pulling price data from FTX API*.
''')

coins = ["BTC/USD", "ETH/USD", "USDT/USD", "BNB/USD", "XRP/USD", "SOL/USD", "DOGE/USD", "DOT/USD", "DAI/USD", "SHIB/USD"]

coin = st.sidebar.selectbox(
    "Choose a coin: ", coins
)

st.title(f"{coin} to USD")
url = f"https//ftx.com/api/markets/{coin}"
request = requests.get(url).json()
data = pd.Series(request["result"])

col1, col2, col3 = st.columns(3)
col1.metric("Price", data['price'], f"{round(data['change24h']*100,2)}%")
col2.metric("Low", data['priceLow'])
col3.metric("High", data['priceHigh'])
val=int(data['volumeUsd'])
st.metric("Volume", f'{val:,}')