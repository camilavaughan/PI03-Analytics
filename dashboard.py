import pandas as pd
import requests
import streamlit as st
from main import get_market_data, api_url
import plotly.graph_objects as go

#Configuramos la página
st.set_page_config(page_title= "camilavaughan", layout= "wide")
st.markdown(''' # **FTX Price App**
A simple cryptocurrency price app pulling price data from FTX API.
''')

coins = ["BTC", "ETH", "USDT", "BNB", "XRP", "SOL", "DOGE", "DOT", "DAI", "SHIB"] 
coin = st.sidebar.selectbox("Choose a coin: ", coins)

url = f"{api_url}/markets/{coin}/USD"
request = requests.get(url).json()
data = pd.Series(request["result"])

col1, col2, col3, col4 = st.columns(4)
price = data["price"]
col1.metric("Price", data["price"])
col2.metric("Low", data["priceLow24h"])
col3.metric("High", data["priceHigh24h"])
col4.metric("Volume", int(data["volumeUsd24h"]))
