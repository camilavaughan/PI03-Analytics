import pandas as pd
import requests
import datetime
import streamlit as st



#Preparando la data a extraer
coins = ["BTC", "ETH", "USDT", "BNB", "XRP", "SOL", "DOGE", "DOT", "DAI", "SHIB"]  #monedas elegidas
api_url = "https://ftx.com/api" #endpoint a utilizar para los demas urls
resolution = (60 * 60 * 24) #seg * min * hs
start_time = datetime.datetime(2022,9,1).timestamp() #inicio del analisis
end_time = datetime.datetime.today().timestamp() #final del analisis


def get_market_data(coin):
    path = f"/markets/{coin}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}"
    url = api_url + path
    request = requests.get(url).json()
    df = pd.DataFrame(request["result"])
    df["date"] = pd.to_datetime(df["startTime"]).dt.date
    df = df.drop(columns=["startTime", "time"])
    return df

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
