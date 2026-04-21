# 🤖 TradeFlow — Binance Futures Testnet Trading Bot

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Binance%20Futures%20Testnet-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Working-brightgreen?style=flat-square)
![Orders](https://img.shields.io/badge/Orders-MARKET%20%7C%20LIMIT%20%7C%20STOP--LIMIT-orange?style=flat-square)

> A clean, production-ready Python CLI application that places **Market**, **Limit**, and **Stop-Limit** orders on **Binance Futures Testnet (USDT-M)** — with structured logging, robust input validation, layered architecture, and clear error handling.

Built as part of the **Primetrade.ai Python Developer Internship** application task.

---

## 📌 Table of Contents

- [Features](#-features)
- [Live Demo](#-live-demo)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Setup](#-setup)
- [How to Run](#-how-to-run)
- [CLI Arguments](#-cli-arguments)
- [Order Types Explained](#-order-types-explained)
- [Validation & Error Handling](#-validation--error-handling)
- [Logging](#-logging)
- [Tech Stack](#-tech-stack)
- [Assumptions](#-assumptions)
- [Future Improvements](#-future-improvements)

---

## ✨ Features

- ✅ Place **MARKET** orders — instant execution at current price
- ✅ Place **LIMIT** orders — execute at your specified price
- ✅ Place **STOP-LIMIT** orders *(bonus)* — trigger-based conditional orders
- ✅ Support for both **BUY** and **SELL** sides
- ✅ Full **input validation** before any API call is made
- ✅ Structured **logging** to rotating file + console (useful, not noisy)
- ✅ Clean **layered architecture** — separate API client, order logic, and CLI layers
- ✅ Graceful **exception handling** — invalid input, HTTP errors, network failures
- ✅ Credentials via **environment variables** (`.env` support)
- ✅ Clear, readable **CLI output** with order summary and response details

---

## ✅ Live Demo

> Real order successfully placed on Binance Futures Testnet:

```
============================================================
📤  ORDER REQUEST SUMMARY
============================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Order Type : MARKET
  Quantity   : 0.01
============================================================
2026-04-21 14:02:38 | INFO | bot.client | [ORDER REQUEST] symbol=BTCUSDT | side=BUY | type=MARKET | qty=0.01
2026-04-21 14:02:39 | INFO | bot.client | [ORDER SUCCESS] orderId=13056999039 | status=NEW | executedQty=0.0000

✅  ORDER RESPONSE
============================================================
  Order ID     : 13056999039
  Status       : NEW
  Executed Qty : 0.0000
  Avg Price    : N/A (pending)
  Client OID   : ScLlAupWbejaiEaWapfbel
============================================================
🎉  Order placed successfully on Binance Futures Testnet!
```

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py             # Package initializer
│   ├── client.py               # Binance REST API wrapper (HMAC-SHA256 signing)
│   ├── orders.py               # Order placement logic + formatted terminal output
│   ├── validators.py           # Input validation for all CLI parameters
│   └── logging_config.py       # Rotating file + console logging setup
├── cli.py                      # Main CLI entry point (argparse)
├── logs/
│   └── trading_bot.log         # Auto-generated, rotating log file
├── .env                        # Your API credentials (never commit this!)
├── .env.example                # Template for environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # You are here!
```

---

## 🏗️ Architecture

TradeFlow follows a clean **3-layer architecture** to separate concerns:

```
┌─────────────────────────────────────────┐
│            CLI Layer (cli.py)           │
│   Parses args → loads credentials →     │
│   calls order layer                     │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│         Order Layer (orders.py)         │
│   Validates input → formats output →    │
│   calls API client                      │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│        API Client Layer (client.py)     │
│   Signs requests (HMAC-SHA256) →        │
│   sends HTTP POST → handles errors      │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│     Binance Futures Testnet REST API    │
│     https://testnet.binancefuture.com   │
└─────────────────────────────────────────┘

         ↕ All layers use ↕
┌─────────────────────────────────────────┐
│       Logging (logging_config.py)       │
│   File handler (DEBUG+) + Console       │
│   handler (INFO+) — rotating 5MB        │
└─────────────────────────────────────────┘
```

**Why this structure?**
- `client.py` only knows about HTTP — nothing about CLI or business logic
- `orders.py` only knows about placing orders — not how args were parsed
- `cli.py` only knows about user input — not about API internals
- Each layer can be tested, replaced, or extended independently

---

## ⚙️ Setup

### Prerequisites
- Python 3.x installed
- pip package manager
- A Binance account (free)

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/TradeFlow.git
cd TradeFlow/trading_bot
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

Dependencies:
```
requests>=2.31.0       # HTTP client for REST API calls
python-dotenv>=1.0.0   # Load credentials from .env file
```

### Step 3 — Get Binance Futures Testnet API credentials

1. Go to **[https://testnet.binancefuture.com](https://testnet.binancefuture.com)**
2. Register a new account (free, no KYC needed)
3. Log in → go to **API Management**
4. Click **Create API** → select **HMAC** as key type
5. Give it a label (e.g. `tradeflow-bot`) → confirm via email/phone
6. **Copy both API Key and Secret Key immediately** — Secret is shown only once!

### Step 4 — Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

> ⚠️ **Never commit `.env` to GitHub!** It's already in `.gitignore`.

---

## 🚀 How to Run

Make sure you're inside the `trading_bot/` directory before running any command.

### Market Order — Execute immediately at current price
```bash
# BUY 0.01 BTC at market price
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# SELL 0.5 ETH at market price
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.5

# SELL 10 DOGE at market price
python cli.py --symbol DOGEUSDT --side SELL --type MARKET --quantity 10
```

### Limit Order — Execute only at your specified price
```bash
# BUY 0.01 BTC when price drops to $60,000
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000

# SELL 0.01 BTC when price rises to $70,000
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000

# BUY 1 ETH at $2,800
python cli.py --symbol ETHUSDT --side BUY --type LIMIT --quantity 1 --price 2800
```

### Stop-Limit Order — Trigger-based conditional order *(Bonus)*
```bash
# BUY 0.01 BTC — activate when price hits $65,000, then limit buy at $65,100
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT \
              --quantity 0.01 --stop-price 65000 --price 65100

# SELL 0.01 BTC — activate at $60,000, limit sell at $59,900 (stop loss)
python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT \
              --quantity 0.01 --stop-price 60000 --price 59900
```

### View help anytime
```bash
python cli.py --help
```

---

## 📋 CLI Arguments

| Argument | Required | Type | Description |
|----------|----------|------|-------------|
| `--symbol` | ✅ Yes | string | Trading pair e.g. `BTCUSDT`, `ETHUSDT`, `DOGEUSDT` |
| `--side` | ✅ Yes | choice | `BUY` or `SELL` |
| `--type` | ✅ Yes | choice | `MARKET`, `LIMIT`, or `STOP_LIMIT` |
| `--quantity` | ✅ Yes | float | Order quantity e.g. `0.01` |
| `--price` | ⚠️ LIMIT/STOP_LIMIT | float | Limit execution price |
| `--stop-price` | ⚠️ STOP_LIMIT only | float | Stop trigger price |
| `--api-key` | ❌ Optional | string | Overrides `BINANCE_API_KEY` env var |
| `--api-secret` | ❌ Optional | string | Overrides `BINANCE_API_SECRET` env var |

---

## 📊 Order Types Explained

### 🟢 MARKET Order
Executes **immediately** at the best available market price. No price input needed.
```
You say:  "Buy 0.01 BTC right now"
Bot does: Places order → fills instantly at current market price (~$75,682)
Use when: You want guaranteed execution, price doesn't matter much
```

### 🟡 LIMIT Order
Executes **only when market reaches your price**. Order stays open (GTC) until filled or cancelled.
```
You say:  "Buy 0.01 BTC only if price drops to $60,000"
Bot does: Places limit order → waits → fills when BTC hits $60,000
Use when: You want a specific entry/exit price
```

### 🔴 STOP-LIMIT Order *(Bonus)*
A two-step conditional order. The **stop price** activates the order, then the **limit price** executes it. Used for stop-losses and breakout strategies.
```
You say:  "If BTC drops to $65,000 (stop), place a sell at $64,900 (limit)"
Bot does: Watches market → triggers at $65,000 → places limit sell at $64,900
Use when: You want automated risk management / breakout trading
```

---

## 🛡️ Validation & Error Handling

Every parameter is validated **before** any API call is made:

| Validation | What it checks | Error example |
|------------|---------------|---------------|
| Symbol | Alphanumeric, non-empty | `"Invalid symbol 'BTC USD'. Must be alphanumeric."` |
| Side | Must be BUY or SELL | `"Invalid side 'buy'. Must be BUY or SELL."` |
| Order Type | Must be MARKET/LIMIT/STOP_LIMIT | `"Invalid order type 'market_order'."` |
| Quantity | Must be > 0 | `"Quantity must be > 0, got -1."` |
| Price | Required + > 0 for LIMIT/STOP_LIMIT | `"Price is required for LIMIT orders."` |
| Stop Price | Required + > 0 for STOP_LIMIT | `"Stop price is required for STOP_LIMIT orders."` |

**Exception handling covers:**
- ❌ Invalid user input → `ValueError` caught, clear message printed, exits cleanly
- ❌ HTTP 400 errors → API error body logged with endpoint info
- ❌ HTTP 401/403 errors → authentication failure logged clearly
- ❌ HTTP 5xx errors → server error logged with context
- ❌ Connection errors → network failure message logged
- ❌ Request timeouts → timeout duration logged
- ❌ Unexpected errors → full traceback in log file, clean message on console

---

## 📄 Logging

All activity is logged to `logs/trading_bot.log` with this format:
```
YYYY-MM-DD HH:MM:SS | LEVEL    | module | message
```

**Sample log output:**
```
2026-04-21 14:02:38 | INFO     | __main__   | Bot started | symbol=BTCUSDT | side=BUY | type=MARKET | qty=0.01
2026-04-21 14:02:38 | DEBUG    | bot.client | POST https://testnet.binancefuture.com/fapi/v1/order
2026-04-21 14:02:38 | INFO     | bot.client | [ORDER REQUEST] symbol=BTCUSDT | side=BUY | type=MARKET | qty=0.01
2026-04-21 14:02:39 | DEBUG    | bot.client | Response [200]: {orderId: 13056999039, status: NEW ...}
2026-04-21 14:02:39 | INFO     | bot.client | [ORDER SUCCESS] orderId=13056999039 | status=NEW | executedQty=0.0000
2026-04-21 14:05:10 | ERROR    | bot.client | HTTP 400 | endpoint=/fapi/v1/order | body={"code":-1121,"msg":"Invalid symbol."}
2026-04-21 14:06:22 | ERROR    | bot.orders | Validation failed: Price is required for LIMIT orders.
```

**Logging design decisions:**
- 📁 **File handler** — captures `DEBUG` and above (full detail for debugging)
- 🖥️ **Console handler** — shows `INFO` and above only (clean, not overwhelming)
- 🔄 **Auto-rotating** — 5 MB max per file, keeps last 3 backups (no disk bloat)
- 🔇 **Not noisy** — logs meaningful events only, not constant polling

---

## 🛠️ Tech Stack

| Component | Tool | Why chosen |
|-----------|------|-----------|
| Language | Python 3.11 | Required by task; excellent ecosystem |
| HTTP Client | `requests` | Industry standard, clean API |
| Authentication | HMAC-SHA256 | Required by Binance REST API |
| CLI | `argparse` (stdlib) | Zero extra dependency, full control |
| Environment | `python-dotenv` | Secure credential management |
| Logging | `logging` stdlib | Built-in rotating file support |
| Exchange API | Binance Futures Testnet | Task requirement |

---

## 📌 Assumptions

- This bot targets **Binance Futures Testnet only** — it is **not** for live trading
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default
- Testnet accounts are pre-funded with virtual USDT — no real money involved
- The bot is a **one-shot order placer** — it does not manage positions, stream live prices, or cancel orders
- Symbol names must match Binance format exactly (e.g., `BTCUSDT` not `BTC/USDT`)
- Minimum order quantities are enforced by Binance API, not this bot

---

## 🔮 Future Improvements

- [ ] Add `--cancel` flag to cancel open orders by order ID
- [ ] Add `--status` flag to query live order status
- [ ] WebSocket support for real-time price streaming
- [ ] Interactive menu mode (no CLI flags needed)
- [ ] OCO (One-Cancels-the-Other) order support
- [ ] TWAP execution strategy
- [ ] Portfolio / position tracking dashboard
- [ ] Unit tests with `pytest` and mocked API responses
- [ ] Docker containerization

---

## 🔐 Security Notes

- API credentials loaded from environment variables — never hardcoded
- `.env` is listed in `.gitignore` — will never be pushed to GitHub
- Secret key is never logged or printed anywhere in the codebase
- Testnet keys cannot access real funds even if compromised

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤️ for Primetrade.ai Python Developer Internship Application Task.*  
*Author: Diksha — [GitHub](https://github.com/Diksha2605)*
