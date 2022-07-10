# https://github.com/dataprofessor/streamlit_freecodecamp/blob/main/app_1_simple_stock_price/myapp.py

import yfinance as yf
import streamlit as st

st.write("""
        # 간단한 주식 가격 앱
        
        Shown are the stock closing price and volume of Goggle
""")

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
