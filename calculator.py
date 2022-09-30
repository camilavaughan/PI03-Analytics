import streamlit as st
import requests
from main import api_url, coins

#Las monedas y el url de la API estan definidos y son traidos desde el archivo "main.py"
def convert_currency(from_currency, to_currency, amount):
    if from_currency == to_currency:    #USD2USD
        if from_currency == "USD" and to_currency == "USD":
            return amount
        else:
            request = requests.get(f"{api_url}/markets/{from_currency}/USD").json()
            price = request["result"]["price"]
            return amount * price
    else:
        if from_currency == "USD":  #USD2COIN
            from_price = 1
            request = requests.get(f"{api_url}/markets/{to_currency}/USD").json()
            to_price = request["result"]["price"]
            return (from_price / to_price) * amount
        elif to_currency == "USD":  #COIN2USD
            request = requests.get(f"{api_url}/markets/{from_currency}/USD").json()
            from_price = request["result"]["price"]
            return from_price * amount
        else:   #COIN2COIN!=USD
            request = requests.get(f"{api_url}/markets/{from_currency}/USD").json()
            from_price = request["result"]["price"]
            request = requests.get(f"{api_url}/markets/{to_currency}/USD").json()
            to_price = request["result"]["price"]
            rate = from_price / to_price
            return amount * rate

st.set_page_config(page_title= "camilavaughan - calculator", layout= "wide")
st.markdown(''' # **FTX Price Calculator**
A simple cryptocurrency calculator pulling price data from FTX API.
''')

col1, col2 = st.columns(2)

market1 = col1.selectbox("Convert from: ", coins, index=1)

market2 = col1.selectbox("To: ", coins, index=0)

amount = col1.number_input("Amount: ", min_value= 0.0, value= 1.0)

col2.metric("Converted value: ", convert_currency(market1, market2, amount))
