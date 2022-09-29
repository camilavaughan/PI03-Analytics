import pandas as pd
import requests
import datetime
import streamlit as st
import plotly.graph_objects as go



#preparando la data a extraer
coins = ["BTC/USD", "ETH/USD", "USDT/USD", "BNB/USD", "XRP/USD", "SOL/USD", "DOGE/USD", "DOT/USD", "DAI/USD", "SHIB/USD"]  #monedas elegidas
api_url = "https://ftx.com/api"
resolution = (60 * 60 * 24) #seg * min * hs
start_time = datetime.datetime(2022,9,1).timestamp() #inicio del analisis
end_time = datetime.datetime.today().timestamp() #final del 


def get_market_data(coin):
    path = f"/markets/{coin}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}"
    url = api_url + path
    res = requests.get(url).json()
    df = pd.DataFrame(res["result"])
    # df.set_index("name", inplace = True)
    df["date"] = pd.to_datetime(df["startTime"])
    df = df.drop(columns=["startTime", "time"])
    df.sort_values("date", inplace=True)
    # name =  market.replace("/", "_")
    return df

