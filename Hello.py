import streamlit as st
import math
from datetime import date, timedelta
import scipy 
from scipy import stats
from scipy.stats import norm
import yfinance as yf
import matplotlib
import py_vollib
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks import analytical
import matplotlib.pyplot as plt
import quandl
##
# Streamlit page setup
st.title('Quantitative Finance: Black Scholes Model for European Option Pricing')

# Quandl API Configuration
quandl.ApiConfig.api_key = 'W-DzNTmgnYb9Kcm-Pirx'

# Default start date setup
default_start_date = date(2024, 5, 1)

# User inputs for stock symbol, strike price, etc.
stock_symbol = st.text_input("Enter the stock symbol (e.g., AAPL for Apple, META for Facebook):", 'AAPL')
K = st.number_input("Enter the strike price:", value=100.0)
T = st.number_input("Enter the duration of the option in years:", value=1.0)
Vol = st.number_input("Enter the volatility as a decimal:", value=0.2)
r = st.number_input("Enter the current risk-free rate as a decimal:", value=0.05)
q = st.number_input("Enter the annual dividend yield as a decimal (e.g., 0.01 for 1%):", value=0.01)

# Selection for call or put option
option_type = st.selectbox("Choose the option type:", ('call', 'put'))

# Date input for stock data
start_date = st.date_input("Select the start date for stock data:", default_start_date)
end_date = st.date_input("Select the end date for stock data:", start_date + timedelta(days=1))

# Fetching real-time stock data
try:
    stock_data = quandl.get("WIKI/" + stock_symbol, start_date=start_date, end_date=end_date)
    if stock_data.empty:
        st.error("No data available for the selected date range. Please choose another date.")
        S = None
    else:
        S = stock_data['Adj. Close'][-1]  # Adjust based on the column name in the dataset
        st.write(f"Current Adjusted Close Price of {stock_symbol}: {S:.2f}")
except Exception as e:
    st.error(f"Error fetching stock data: {e}")
    S = None

if S is not None:
    # Adjust stock price for dividends
    S_adjusted = S * math.exp(-q * T)

    # Calculating d1 and d2
    def calculate_d1_d2(S, K, T, r, Vol):
        d1 = (math.log(S/K) + (r + (Vol**2) / 2) * T) / (Vol * math.sqrt(T))
        d2 = d1 - Vol * math.sqrt(T)
        return d1, d2

    d1, d2 = calculate_d1_d2(S_adjusted, K, T, r, Vol)

    # Black-Scholes Model for Call and Put
    def black_scholes_option(S, K, T, r, Vol, d1, d2, option_type):
        if option_type == 'call':
            price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)
        return price

    option_price = black_scholes_option(S_adjusted, K, T, r, Vol, d1, d2, option_type)
    st.write(f"{option_type.capitalize()} Option Price: {option_price:.2f}")

    # Display Greeks using adjusted S
    def display_greeks(flag, S, K, T, r, Vol):
        greeks = {
            "Delta": analytical.delta(flag, S, K, T, r, Vol),
            "Gamma": analytical.gamma(flag, S, K, T, r, Vol),
            "Theta": analytical.theta(flag, S, K, T, r, Vol),
            "Vega": analytical.vega(flag, S, K, T, r, Vol),
            "Rho": analytical.rho(flag, S, K, T, r, Vol)
        }
        st.subheader(f"{option_type.capitalize()} Option Greeks")
        for greek, value in greeks.items():
            if option_type == 'call' and greek in ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']:
                st.markdown(f"**{greek}:** `{value:.4f}`", unsafe_allow_html=True)
            else:
                st.write(f"{greek}: {value:.4f}")
        return greeks
    greeks = display_greeks(option_type[0], S_adjusted, K, T, r, Vol)



