# 📊 Order Book Imbalance Tracker

A real-time crypto trading tool that connects to **Binance WebSocket**, streams live order book data, calculates **bid/ask imbalance**, and prints buy/sell pressure signals directly in your terminal — with zero paid APIs and minimal dependencies.

---

## 🧠 What Is Order Book Imbalance?

Every crypto exchange maintains an **order book** — a live list of all pending buy and sell orders:

| Side | What it represents |
|------|--------------------|
| **Bids** | Buyers waiting to purchase at a price (demand) |
| **Asks** | Sellers waiting to sell at a price (supply)    |

**Order Book Imbalance (OBI)** measures the *relative weight* of buyers vs sellers at any moment:

```
Imbalance Ratio = Total Bid Volume / (Total Bid Volume + Total Ask Volume)
```

| Ratio     | Interpretation         | Signal          |
|-----------|------------------------|-----------------|
| > 0.60    | More buyers than sellers | 🟢 BUY PRESSURE  |
| < 0.40    | More sellers than buyers | 🔴 SELL PRESSURE |
| 0.40–0.60 | Balanced market          | ⚪ NEUTRAL        |

---

## 💡 Why Does This Matter in Trading?

Order book imbalance is one of the **earliest signals** of short-term price movement — often appearing *before* the price actually moves.

Here's the intuition:

- If there are **10× more buyers than sellers** in the top 10 levels, market makers will lift their ask prices because demand is strong. **Price tends to rise.**
- If sellers are **stacking up** with little buy support beneath, prices are likely to drop as buyers get filled and sellers keep entering.

**Who uses this?**
- High-Frequency Trading (HFT) firms use imbalance as a core input
- Market makers use it to adjust their quotes in real time
- Short-term traders use it to confirm momentum before entering a trade
- Quant researchers use logged imbalance data to build predictive models

This project gives you a working foundation to **observe, log, and eventually model** this signal.

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/order-book-imbalance-tracker.git
cd order-book-imbalance-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the tracker
```bash
# Default: BTCUSDT, top 10 levels
python main.py

# Track Ethereum
python main.py --symbol ethusdt

# Use top 5 levels only
python main.py --symbol solusdt --levels 5

# Disable CSV logging
python main.py --no-log
```

> **No API key required.** Binance's depth stream is completely public.

---

## 📺 Sample Output

```
=======================================================
  📊 Order Book Imbalance Tracker
  Symbol : BTCUSDT
  Levels : Top 10 bid/ask levels
  Source : Binance WebSocket (live)
=======================================================
  TIME        BID VOL    ASK VOL   RATIO  SIGNAL
-------------------------------------------------------
  14:23:01     12.4821     8.3047  0.6005  BUY PRESSURE 🟢
  14:23:01     13.1004     7.9210  0.6232  BUY PRESSURE 🟢
  14:23:02     10.5533    11.2891  0.4832  NEUTRAL  ⚪
  14:23:02      8.1204    14.9902  0.3513  SELL PRESSURE 🔴
  14:23:03      9.3310    13.7741  0.4037  NEUTRAL  ⚪
```

---

## 📁 Project Structure

```
order-book-imbalance-tracker/
│
├── main.py                  # Entry point — WebSocket connection & streaming loop
│
├── src/
│   ├── imbalance.py         # Core imbalance calculation & signal logic
│   ├── display.py           # Terminal formatting & output helpers
│   └── logger.py            # CSV logger (saves signals to logs/signals.csv)
│
├── tests/
│   └── test_imbalance.py    # Unit tests for imbalance logic
│
├── logs/
│   └── signals.csv          # Auto-generated at runtime (gitignored)
│
├── requirements.txt         # Only 1 external library (websocket-client)
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

```
Binance WebSocket
      │
      │  streams depth update every 100ms
      ▼
  on_message()  ← main.py
      │
      │  passes bids[], asks[] (top 10 levels)
      ▼
  calculate_imbalance()  ← src/imbalance.py
      │
      │  returns ratio + signal
      ▼
  print_snapshot()       ← src/display.py   (terminal)
  log_snapshot()         ← src/logger.py    (CSV file)
```

Each module does **one thing only** — making the code easy to read, test, and extend.

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

Tests cover buy pressure, sell pressure, neutral market, empty book edge case, and level slicing.

---

## 📈 Ideas to Extend This Project

| Extension | Difficulty |
|-----------|------------|
| Plot imbalance ratio over time with `matplotlib` | ⭐ Easy |
| Alert via Telegram when ratio crosses 0.7 / 0.3 | ⭐⭐ Medium |
| Correlate imbalance with 1-min price change | ⭐⭐ Medium |
| Track multiple symbols simultaneously | ⭐⭐ Medium |
| Build a backtester using logged CSV data | ⭐⭐⭐ Hard |
| Add weighted imbalance (weight by proximity to mid price) | ⭐⭐⭐ Hard |

---

## 📦 Dependencies

| Library | Purpose | Version |
|---------|---------|---------|
| `websocket-client` | Connect to Binance WebSocket | 1.8.0 |
| `pytest` | Run unit tests (optional) | 8.3.5 |

Python's built-in `json`, `csv`, `os`, `argparse`, `datetime` modules handle everything else.

---

## 🔗 Data Source

This project uses **Binance's free public WebSocket API**:

```
wss://stream.binance.com:9443/ws/{symbol}@depth{levels}@100ms
```

- No authentication needed
- Updates every 100 milliseconds
- Supports all Binance spot trading pairs

Full documentation: [Binance WebSocket Streams](https://binance-docs.github.io/apidocs/spot/en/#partial-book-depth-streams)

---

## 👤 Author

Built as part of a crypto trading tools portfolio.  
Feel free to fork, extend, and use in your own projects.

---

## 📄 License

MIT License — free to use for personal and commercial projects.
