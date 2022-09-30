import pandas as pd
import requests
import streamlit as st
from main import get_market_data, api_url, coins
import plotly.graph_objects as go

#Configuramos la página
st.set_page_config(page_title= "camilavaughan", layout= "wide")
st.markdown(''' # **FTX Price App**
A simple cryptocurrency price app pulling price data from FTX API.
''')

coin = st.sidebar.selectbox("Choose a coin: ", coins)

url = f"{api_url}/markets/{coin}/USD"
request = requests.get(url).json()
data = pd.Series(request["result"])

col1, col2, col3 = st.columns(3)
price = data["price"]
col1.metric("Price", data['price'], f"{round(data['change24h']*100,2)}%")
col2.metric("Low", data['low'])
col3.metric("High", data['high'])
val=int(data['volumeUsd'])
st.metric("Volume", f'{val:,}')