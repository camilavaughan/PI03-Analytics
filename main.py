import pandas as pd
import requests
import datetime
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#Preparando la data a extraer
coins = ["BTC", "ETH", "USDT", "BNB", "XRP", "SOL", "DOGE", "DOT", "DAI", "SHIB"]  #monedas elegidas
api_url = "https://ftx.com/api"
resolution = (60 * 60) #seg * min
start_time = datetime.datetime(2022,9,1).timestamp() #inicio del analisis
end_time = datetime.datetime.today().timestamp() #final del analisis


def get_market_data(coin):
    path = f"https://ftx.com/api/markets/{coin}/USD/candles?resolution={resolution}"
    request = requests.get(path).json()
    dfdata = pd.DataFrame(request['result'])
    dfdata["date"] = pd.to_datetime(dfdata["startTime"]).dt.date
    dfdata = dfdata.drop(columns=["startTime", "time"])
    return dfdata

#Parte gráfica / Streamlit
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


def candlestick_plot(
    df: pd.DataFrame,
    ma1: int,
    ticker: str):

    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.2,
        subplot_titles = (f'{ticker} Price', 'Volume'),
        row_width = [5, 10]
    )
    fig.add_trace(
        go.Candlestick(
            x = df['date'],
            open = df['open'], 
            high = df['high'],
            low = df['low'],
            close = df['close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    fig.add_trace(
        go.Line(x = df['date'], y = df[f'{ma1}_ma'], name = f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    fig.add_trace(
        go.Bar(x = df['date'], y = round(df['volume'],2), name = 'Volume'),
        row = 2,
        col = 1,
    )
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    fig.update_xaxes(
        rangeslider_visible = False,
    )
    
    return fig

dfhistorical = get_market_data(coin)
ma1 = st.sidebar.number_input("Moving Average",value=100, min_value=0, max_value=1200, step=1)
dfhistorical[f"{ma1}_ma"] = dfhistorical["close"].rolling(ma1).mean()
st.plotly_chart(candlestick_plot(dfhistorical, ma1, coin), use_container_width= True)