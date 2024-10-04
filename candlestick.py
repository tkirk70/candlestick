import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots

st.title("Stock Candlestick Chart")

# List of stock tickers
tickers = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA", "INTC"]

# Sidebar for selecting the stock
selected_stock = st.sidebar.selectbox("Select a stock", tickers)

# Get stock data from Yahoo Finance
stock_data = yf.download(selected_stock, start="2023-01-01", threads=False)

# Create subplots with shared x-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                    subplot_titles=(f"{selected_stock} OHLC", "Volume"))

# Add candlestick trace
fig.add_trace(go.Candlestick(x=stock_data.index,
                             open=stock_data["Open"],
                             high=stock_data["High"],
                             low=stock_data["Low"],
                             close=stock_data["Close"],
                             name="Candlestick"),
              row=1, col=1)

# Add volume trace
fig.add_trace(go.Bar(x=stock_data.index,
                     y=stock_data["Volume"],
                     name="Volume",
                     marker_color="blue"),
              row=2, col=1)

# Customize chart layout
fig.update_xaxes(title_text="Date",
                 rangeslider_visible=False,
                 rangeselector=dict(buttons=list([
                     dict(count=1, label="1M", step="month", stepmode="backward"),
                     dict(count=6, label="6M", step="month", stepmode="backward"),
                     dict(count=1, label="YTD", step="year", stepmode="todate"),
                     dict(count=1, label="1Y", step="year", stepmode="backward"),
                     dict(step="all")
                 ])))

fig.update_layout(title=f"{selected_stock} Share Price and Volume (2023-Today)",
                  title_y=0.9,
                  title_x=0.5,
                  title_xanchor="center",
                  title_yanchor="top",
                  height=1000,
                  width=1200)

fig.update_yaxes(title_text=f"{selected_stock} Close Price", tickprefix="$", row=1, col=1)
fig.update_yaxes(title_text=f"{selected_stock} Volume", tickprefix=" ", row=2, col=1)

# Set y-axis range for each subplot
fig.update_yaxes(range=[min(stock_data["Low"]), max(stock_data["High"])], row=1, col=1)
fig.update_yaxes(range=[min(stock_data["Volume"]), max(stock_data["Volume"])], row=2, col=1)
# fig.update_yaxes(range=[165, 205], row=1, col=1)
# fig.update_yaxes(autorange=True, row=2, col=1)

# Display the chart in Streamlit
st.plotly_chart(fig)
