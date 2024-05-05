import streamlit as st
import math
import googlefinance
from datetime import date, timedelta
import scipy 
from scipy import stats
from scipy.stats import norm
import yfinance as yf
import matplotlib
import py_vollib
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks import analytical
import pandas_datareader.data as web
##
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
    stock_data = web.DataReader(stock_symbol, 'yahoo', start_date, end_date)
    # Check if data frame is not empty and column exists
    if not stock_data.empty and 'Adj Close' in stock_data.columns:
        S = stock_data['Adj Close'][-1]
        st.write(f"Current Adjusted Close Price of {stock_symbol}: {S:.2f}")
    else:
        st.error("No data available for the selected date range or missing 'Adj Close'. Please choose another date.")
        S = None
except Exception as e:
    st.error(f"Error fetching stock data: {str(e)}")
    S = None

# Handling when S is not None to proceed with further calculations (add your option pricing calculations here)
if S is not None:
    # (Continue with your Black-Scholes calculations and other code as before)
    pass

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



