import streamlit as st
import requests


def convert_currency(from_currency, to_currency, amount):
    
    if from_currency == to_currency:    #USD2USD
        if from_currency == "USD" and to_currency == "USD":
            return amount
        else:
            request = requests.get(f"https://ftx.com/api/markets/{from_currency}/USD").json()
            price = request["result"]["price"]
            return amount * price
    else:
        if from_currency == "USD":  #USD2COIN
            from_price = 1
            request = requests.get(f"https://ftx.com/api/markets/{to_currency}/USD").json()
            to_price = request["result"]["price"]
            return (from_price/to_price) * amount
        elif to_currency == "USD":  #COIN2USD
            request = requests.get(f"https://ftx.com/api/markets/{from_currency}/USD").json()
            from_price = request["result"]["price"]
            return from_price * amount
        else:   #COIN2COIN!=USD
            request = requests.get(f"https://ftx.com/api/markets/{from_currency}/USD").json()
            from_price = request["result"]["price"]
            request = requests.get(f"https://ftx.com/api/markets/{to_currency}/USD").json()
            to_price = request["result"]["price"]
            rate = from_price / to_price
            return amount * rate


st.title("Currency converter")

markets = ["BTC", "ETH", "USDT", "BNB", "XRP", "SOL", "DOGE", "DOT", "DAI", "SHIB"]

col1, col2 = st.columns(2)

market1 = col1.selectbox("Convert", markets, index=1)

market2 = col1.selectbox("To", markets, index=0)

amount = col2.numberinput("Amount", min_value= 0.0, value= 1.0)
col2.metric("Converted", convert_currency(market1, market2, amount))
