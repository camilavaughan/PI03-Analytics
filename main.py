import pandas as pd
import requests
import datetime
import streamlit as st
import plotly.graph_objects as go


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
    df["date"] = pd.to_datetime(df["startTime"])
    df = df.drop(columns=["startTime", "time"])
    df.sort_values("date", inplace=True)
    return df