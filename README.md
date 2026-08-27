## 🤖 Mini Trading Bot - Educational Paper Trading Simulator

A simple Python trading bot for **educational purposes** that simulates trading on historical data. **NO REAL MONEY IS INVOLVED.**

### ⚠️ Important Disclaimer

- This is for **learning only**
- This is **NOT financial advice**
- Past performance does not guarantee future results
- Most retail traders lose money
- Never invest money you can't afford to lose

---

## 📋 What This Bot Does

1. **Downloads historical price data** from Yahoo Finance
2. **Calculates moving averages** (20-day and 50-day)
3. **Uses a simple strategy**: Buy when short MA crosses above long MA (Golden Cross), Sell when it crosses below (Death Cross)
4. **Simulates trades** on historical data and tracks profit/loss
5. **Reports results**: Shows final profit/loss and win rate

---

## 🚀 How to Run

### 1. Install Python (if you don't have it)
Download from [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Bot
```bash
python bot.py
```

You'll see output like:
```
✅ BUY  - 2023-01-15 @ $16580.45 | Bought 0.060305 BTC-USD
🔴 SELL - 2023-02-28 @ $23561.23 | Profit/Loss: $421.95 (42.19%)
```

---

## 📊 What You'll Learn

- How to fetch financial data with Python
- How to calculate technical indicators (moving averages)
- How to implement trading strategies
- How to backtest on historical data
- Basic Python programming with real data

---

## 🎯 Strategy Explained

**Moving Average Crossover:**
- **SMA_20**: Average price over last 20 days (fast)
- **SMA_50**: Average price over last 50 days (slow)

**Buy Signal**: When SMA_20 crosses ABOVE SMA_50 (Golden Cross)
- Shows upward momentum
- Time to buy

**Sell Signal**: When SMA_20 crosses BELOW SMA_50 (Death Cross)
- Shows downward momentum
- Time to sell

---

## 🛠️ How to Modify

### Change the Asset
```python
# In bot.py, line 128
symbol="ETH-USD"  # Trade Ethereum instead
# or "AAPL", "GOOGL", "SPY", etc.
```

### Change the Capital
```python
# In bot.py, line 127
initial_capital=5000  # Start with $5000 instead
```

### Change the Period
```python
# In bot.py, lines 129-130
start_date=datetime(2022, 1, 1),
end_date=datetime(2024, 8, 27)
```

### Change the Strategy
Edit the `_should_buy()` and `_should_sell()` methods to implement different signals!

---

## 📈 Understanding Results

After running, you'll see:
- **Initial Capital**: How much you started with
- **Final Value**: How much you'd have after all trades
- **Total Return**: Profit/Loss in dollars and percentage
- **Win Rate**: % of trades that were profitable

---

## ⚡ Next Steps

1. **Run the bot** on different assets
2. **Try different time periods**
3. **Modify the strategy** (change indicators)
4. **Backtest** on more historical data
5. **Learn more** about trading, Python, and finance

---

## 🔗 Resources

- [Python Documentation](https://docs.python.org/)
- [pandas Documentation](https://pandas.pydata.org/)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Moving Averages Explained](https://www.investopedia.com/terms/m/movingaverage.asp)
- [Trading Strategy Basics](https://www.investopedia.com/articles/trading/03/082703.asp)

---

## 📝 License

Educational use only. See LICENSE file.

---

**Remember**: This is a learning tool. Real trading involves risk. Start with paper trading, never risk money you can't afford to lose, and always do your own research! 🎓
