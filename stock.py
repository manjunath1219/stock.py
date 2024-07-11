import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

data = pd.read_csv(r"C:\Users\manju\OneDrive\Desktop\TCS_stock_history.csv")
st.dataframe(data)
data['Date'] = pd.to_datetime(data['Date'])
st.line_chart(data, x ='Date', y = 'Close' )

#################

fig = go.Figure()
fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']) )
st.plotly_chart(fig)

#####################

data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()
st.line_chart(data[['Close', 'MA20', 'MA50']])

#############

fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'))
fig.update_layout(
    title='Trading Volume Over Time',
    xaxis_title='Date',
    yaxis_title='Volume',
    legend_title='Legend'
)
st.plotly_chart(fig)

#####################

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

######################
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

####################################

data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
st.heatmap(Date=data.Date,
                       data=data,
                       month_grid=True,
                       horizontal=True,
                       value_label=True,
                       date_label=False,
                       weekday_label=True,
                       month_label=True,
                       year_label=True,
                       colorbar=True,
                       fontfamily="monospace",
                       fontsize=12)