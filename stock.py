###  Import the libraries  ###

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

### Step 1: Loading the Data
    
st.file_uploader("Upload your input file", type=["csv"], key="uploaded_file")
data = pd.read_table(st.session_state["uploaded_file"] , sep=",", header=0)
st.title(data)
st.dataframe(data)

### Step 2: Data Cleaning

st.title('Print missing values')
missing_values = data.isnull().sum()
st.dataframe(missing_values)

### Drop missing values
st.title('Data after droping missing values')
data = data.drop(['Dividends', 'Stock Splits'], axis=1)
st.dataframe(data)

### Displaying Stock Price Movements

st.title('Plotting Stock Price Movements')
data['Date'] = pd.to_datetime(data['Date'])
st.line_chart(data, x ='Date', y = 'Close' )

### Displaying Candlestick Chart

st.title('Candlestick Chart')
fig = go.Figure()
fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']) )
st.plotly_chart(fig)

### Adding Moving Averages

st.title('Moving Averages')
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()
st.line_chart(data[['Close', 'MA20', 'MA50']])

### Analyzing Trading Volumes

st.title('Trading Volumes Chart')
fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'))
fig.update_layout(
    title='Trading Volume Over Time',
    xaxis_title='Date',
    yaxis_title='Volume',
    legend_title='Legend'
)
st.plotly_chart(fig)

### Combined Price and Volume Chart

st.title('Price and Volume in one chart')
fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True,
    vertical_spacing=0.1, subplot_titles=('OHLC', 'Volume'),
    row_width=[0.2, 0.7]
)

# Add candlestick chart
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name='Candlestick'
), row=1, col=1)

# Add volume bar chart
fig.add_trace(go.Bar(
    x=data.index, y=data['Volume'], name='Volume'
), row=2, col=1)

# Update layout
fig.update_layout(
    title='Stock Price and Volume',
    xaxis_title='Date',
    yaxis_title='Price',
    yaxis2_title='Volume'
)

# Display plot in Streamlit
st.plotly_chart(fig)

### Distribution of Daily Returns

st.title('Distribution of Daily Returns')

# Calculate Daily Returns
data['Daily Return'] = data['Close'].pct_change()

# Drop NaN values for plotting
daily_returns = data['Daily Return'].dropna()

# Plotly Histogram with KDE
fig = ff.create_distplot(
    [daily_returns], 
    group_labels=['Daily Return'], 
    bin_size=0.01, 
    show_rug=False
)
fig.update_layout(
    title='Distribution of Daily Returns',
    xaxis_title='Daily Return',
    yaxis_title='Frequency'
)

# Display plot in Streamlit
st.plotly_chart(fig)

