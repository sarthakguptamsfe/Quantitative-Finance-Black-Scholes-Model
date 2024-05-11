import streamlit as st
import math
import requests
from datetime import date, timedelta
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks import analytical

st.set_page_config(page_title="Quantitative Finance: Black Scholes Model")
# Display the header image
image_url = "https://i.postimg.cc/bvqxzkwp/abc.jpg"
st.image(image_url, use_column_width=True)
# API key for FinancialModelingPrep
API_KEY = '0uTB4phKEr4dHcB2zJMmVmKUcywpkxDQ'

# User inputs for option pricing
stock_symbol = st.text_input("Enter the stock symbol (e.g., AAPL for Apple, META for Facebook):", 'AAPL')
default_date = date(2024, 5, 1)
selected_date = st.date_input("Select the date for fetching the stock price:", default_date)
K = st.number_input("Enter the strike price:", value=100.0)
option_type = st.selectbox("Choose the option type:", ('call', 'put'))
days = st.number_input("Enter the duration of the option in days:", min_value=1, max_value=3650, value=1, step=1)
T = days / 365.25  # Convert days to years for the formula
Vol = st.number_input("Enter the volatility as a decimal:", value=0.2)
r = st.number_input("Enter the current risk-free rate as a decimal:", value=0.05)
q = st.number_input("Enter the annual dividend yield as a decimal (e.g., 0.01 for 1%):", value=0.01)



# Fetching real-time stock data
try:
    response = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock_symbol}?from={selected_date}&to={selected_date}&apikey={API_KEY}")
    data = response.json()
    if 'historical' not in data or not data['historical']:
        st.error("No data available for the selected date. Please choose another date.")
        S = None
    else:
        S = data['historical'][0]['close']  # Fetch the closing price of the selected date
        st.subheader(f"Stock Price of {stock_symbol} on {selected_date}: {S:.2f}")
except Exception as e:
    st.error(f"Error fetching stock data: {str(e)}")
    S = None

# Function to calculate d1 and d2
def calculate_d1_d2(S, K, T, r, Vol):
    d1 = (math.log(S / K) + (r + 0.5 * Vol**2) * T) / (Vol * math.sqrt(T))
    d2 = d1 - Vol * math.sqrt(T)
    return d1, d2

# Further processing only if S is not None
if S is not None:
    S_adjusted = S * math.exp(-q * T)
    
    # Calculate d1 and d2
    d1, d2 = calculate_d1_d2(S_adjusted, K, T, r, Vol)

    # Calculate option price based on type
    if option_type == 'call':
        price = S_adjusted * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S_adjusted * norm.cdf(-d1)

    st.subheader(f"{option_type.capitalize()} Option Price: {price:.2f}")
    # Display Greeks
    greeks = {
        "Delta": analytical.delta(option_type[0], S_adjusted, K, T, r, Vol),
        "Gamma": analytical.gamma(option_type[0], S_adjusted, K, T, r, Vol),
        "Theta": analytical.theta(option_type[0], S_adjusted, K, T, r, Vol),
        "Vega": analytical.vega(option_type[0], S_adjusted, K, T, r, Vol),
        "Rho": analytical.rho(option_type[0], S_adjusted, K, T, r, Vol)}
    st.subheader(f"{option_type.capitalize()} Option Greeks")
    for greek, value in greeks.items():
        st.write(f"**{greek}:** {value:.4f}")
