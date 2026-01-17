# btc-algorithmic-trading-backtester
Interactive algorithmic trading backtester for Bitcoin with SMA &amp; RSI strategies using Streamlit
# 📈 BTC Algorithmic Trading Strategy Backtester

An interactive **algorithmic trading backtester** built in **Python** that allows users to evaluate **SMA (trend-following)** and **RSI (mean-reversion)** swing trading strategies on **Bitcoin (BTC)** historical data.

The project includes a **Streamlit dashboard** where users can configure strategy parameters, initial capital, and date ranges, and instantly view performance metrics and equity curves.

---

## 🚀 Features

- 📊 Backtest Bitcoin trading strategies on historical data
- 🔁 Multiple strategies:
  - Simple Moving Average (SMA)
  - Relative Strength Index (RSI)
- ⚙️ Customizable parameters:
  - Initial capital
  - SMA window size
  - RSI upper & lower thresholds
  - Start date & end date
- 💰 Performance metrics:
  - Total Profit & Loss
  - Return percentage
  - Equity curve visualization
  - Win rate
  - Maximum drawdown
- 🖥️ Interactive Streamlit dashboard
- 📉 Clean buy/sell signal visualization

---

## 🧠 Strategy Logic

### 🔹 SMA Strategy (Trend-Following)
- **Buy** when price crosses above the SMA
- **Sell** when price crosses below the SMA
- Long-only swing trading strategy

### 🔹 RSI Strategy (Mean-Reversion)
- **Buy** when RSI falls below lower threshold (e.g. 30)
- **Sell** when RSI rises above upper threshold (e.g. 70)
- Uses signal-based exits instead of fixed stop-loss or targets

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- yfinance

---

## ▶️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/btc-algorithmic-trading-backtester.git
cd btc-algorithmic-trading-backtester
