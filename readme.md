## 📈 Algo-Trading System Dashboard - Introduction

This is a Stock Price Prediction and Analysis dashboard which helps the user know about the latest stock market conditions by generating portfolio analytics like **Last Trade Log** and **P&L Summary** and Buy/Sell signals  of a specific stock using Machine Learning automation by analyzing the latest stock market data. This benefits the user by signalling him the right time to buy and sell stocks, making more profits without any major risk.

## Features

- Connects to Alpha Vantage, a Stock Data API for latest stock market data retrieval of three NIFTY 50 companies i.e., Reliance, Infosys and HDFC bank.
- Analyzes the data using parameters like opening, closing, highest and lowest prices and volume of the stock.
-  Implements Trading Strategy logic by
    - Indicating RSI (Relative Strength Index) value less than 30 as a buy signal
    - Confirming with DMA (Displaced Moving Average) value of 20 crossing above 50 
    - Backtesting for 6 months
    - Building Random Forest Regressor Model to predict next-day movement using values like RSI, MACD (Moving Average Convergence Divergence), Volume, etc.
- Generates portfolio analytics like Trade Log and P&L (Profit and Loss) Summary using Streamlit dashboard.
- Stores Last Trade Log, P&L Summary and Win Ratio in Google Sheets for further analysis.

## Technologies Used

- **Python** for Programming and Model Training
- **Alpha Vantage API** for latest stock market data
- **Random Forest Regressor** for predicting next-dat movements
- **Streamlit** dashboard for generating portfolio analytics
- **Google Sheets** API for storing generated analytics 

## Future Enhancements

- Visualizing Analytics using charts and graphs
- Adding Telegram alert integration for signal alerts or error notifications.