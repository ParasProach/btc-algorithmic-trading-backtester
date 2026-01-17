import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


st.set_page_config(page_title="BTC Strategy Backtester", layout="wide")

st.title("📈 BTC Algorithmic Trading Strategy Backtester")

# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.header("Strategy Settings")
st.sidebar.header("Backtest Settings")

start_date = st.sidebar.date_input(
    "Start Date",
    value=date(2020, 1, 1),
    min_value=date(2015, 1, 1),
    max_value=date.today()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date.today(),
    min_value=start_date,
    max_value=date.today()
)

initial_capital = st.sidebar.number_input(
    "Initial Capital ($)",
    min_value=1000,
    max_value=10_000_000,
    value=1_000_000,
    step=10000
)

strategy = st.sidebar.selectbox(
    "Choose Strategy",
    ["SMA", "RSI"]
)

# Strategy-specific parameters
if strategy == "SMA":
    sma_window = st.sidebar.slider(
        "SMA Window",
        min_value=5,
        max_value=200,
        value=20
    )
else:
    rsi_lower = st.sidebar.slider(
        "RSI Lower Threshold",
        min_value=10,
        max_value=40,
        value=30
    )
    rsi_upper = st.sidebar.slider(
        "RSI Upper Threshold",
        min_value=60,
        max_value=90,
        value=70
    )

# =========================
# DATA DOWNLOAD
# =========================

@st.cache_data
def load_data(start, end):
    data = yf.download("BTC-USD", start=start, end=end)
    data.columns = data.columns.get_level_values(0)
    return data


data = load_data(start_date, end_date).copy()

# =========================
# INDICATORS & SIGNALS
# =========================

if strategy == "SMA":
    data["SMA"] = data["Close"].rolling(sma_window).mean()
    data.dropna(inplace=True)

    data["Signal"] = np.where(data["Close"] > data["SMA"], 1, -1)
    data["Signal_Change"] = data["Signal"].diff()

else:
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    data.dropna(inplace=True)

    data["Signal"] = np.nan
    data.loc[data["RSI"] < rsi_lower, "Signal"] = 1
    data.loc[data["RSI"] > rsi_upper, "Signal"] = -1
    data["Signal"] = data["Signal"].ffill()
    data["Signal_Change"] = data["Signal"].diff()

# =========================
# BACKTEST ENGINE
# =========================

cash = initial_capital
position = 0
portfolio_values = []

for i in range(len(data)):
    price = data["Close"].iloc[i]
    signal_change = data["Signal_Change"].iloc[i]

    if signal_change == 2 and cash > 0:
        position = cash / price
        cash = 0

    elif signal_change == -2 and position > 0:
        cash = position * price
        position = 0

    portfolio_values.append(cash + position * price)

data["Portfolio_Value"] = portfolio_values

# =========================
# METRICS
# =========================

final_value = data["Portfolio_Value"].iloc[-1]
total_pnl = final_value - initial_capital
return_pct = (total_pnl / initial_capital) * 100

# =========================
# DASHBOARD OUTPUT
# =========================

col1, col2, col3 = st.columns(3)

col1.metric("Initial Capital", f"${initial_capital:,.0f}")
col2.metric("Final Value", f"${final_value:,.0f}")
col3.metric("Return (%)", f"{return_pct:.2f}%")

# =========================
# EQUITY CURVE
# =========================

st.subheader("📊 Equity Curve")

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(data.index, data["Portfolio_Value"])
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Value ($)")
ax.grid(alpha=0.3)
st.pyplot(fig)

# =========================
# PRICE & SIGNALS
# =========================

st.subheader("📉 Price Chart with Trade Signals")

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(data.index, data["Close"], label="BTC Price")

if strategy == "SMA":
    ax.plot(data.index, data["SMA"], label=f"SMA {sma_window}", alpha=0.5)

ax.scatter(
    data.index[data["Signal_Change"] == 2],
    data["Close"][data["Signal_Change"] == 2],
    marker="^", color="green", label="BUY"
)

ax.scatter(
    data.index[data["Signal_Change"] == -2],
    data["Close"][data["Signal_Change"] == -2],
    marker="v", color="red", label="SELL"
)

ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)
