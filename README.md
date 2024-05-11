# [Quantitative Finance: Black Scholes Model](https://black-scholes-model.streamlit.app/)

## Overview
This interactive web application leverages the Black Scholes Model to calculate the pricing of European call and put options. Aimed at students, educators, and finance professionals, it provides real-time insights into option valuation and the sensitivity of the option's price to model inputs, commonly known as the "Greeks".

## Features
- **Real-Time Stock Price Fetching**: Utilizes the Financial Modeling Prep API to retrieve the latest stock prices for accurate option pricing.
- **Option Pricing**: Calculate the price of call and put options using the Black Scholes formula.
- **Sensitivity Analysis (Greeks)**: Displays Delta, Gamma, Theta, Vega, and Rho, providing insights into how different factors affect the price of the option.
- **Interactive User Inputs**: Allows users to specify stock symbol, strike price, option type, duration, volatility, risk-free rate, and dividend yield.
- **Error Handling**: Provides feedback when data is unavailable or inputs are invalid.

## Technologies
- **Streamlit**: For creating a user-friendly and interactive web interface.
- **Python**: Handles computational logic, including financial calculations and data fetching.
- **Requests**: Manages HTTP requests to the Financial Modeling Prep API for real-time data.
- **SciPy**: Used for statistical functions, particularly for calculating the cumulative distribution function needed in the Black Scholes formula.
- **py_vollib**: A Python library used for calculating Black Scholes pricing and the Greeks.

## API Key
You will need an API key from [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/) to fetch stock data. Insert the API key in the `API_KEY` variable within the script.

## Contributing
We encourage contributions from the community, whether they are feature improvements, bug fixes, or documentation enhancements. Follow these steps to contribute:

1. **Fork the Repository**: Fork the project to your GitHub account.
2. **Clone Your Fork**: Download your fork to your computer.
3. **Create a New Branch**: Switch to a new branch for your changes.
4. **Make Changes**: Implement your changes or improvements.
5. **Commit Your Changes**: Save your changes with a clear commit message.
6. **Push to GitHub**: Upload the changes to your fork.
7. **Submit a Pull Request**: Open a pull request from your branch to the main project.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For support, raise an issue on the GitHub repository. We aim to address issues promptly and help resolve any challenges users may face.

Thank you for using or contributing to the Quantitative Finance: Black Scholes Model application!

