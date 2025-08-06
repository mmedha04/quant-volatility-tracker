# Options Volatility Tracker

The Options Volatility Tracker is a command-line Python tool that fetches real-time options data and historical stock prices to detect key volatility-based market signals.

Built to simulate the early stages of quantitative research, it helps flag periods of unusual market activity using implied volatility (IV), historical volatility (HV), and price behavior.

---

## Features

- Fetches real-time implied volatility (IV) from options chains using `yfinance`
- Downloads recent stock price history for custom time windows
- Detects and logs market signals:
  - IV Spike Detection
  - IV vs Historical Volatility Ratio
  - IV–Price Divergence
- Logs signal messages to:
  - Terminal
  - `logs/app.log` (structured logging)
  - `data/signals.csv` (CSV signal log)
- Modular architecture with CLI support and extensible signal system

---

## How to Run

## 1. Clone the repository

```bash
git clone https://github.com/mmedha04/options-volatility-tracker.git
cd options-volatility-tracker/src
```


## 2. Set up virtual environment
```bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```
   

## 3. Run the script
```bash
python main.py --ticker AAPL --days 31 
```


## Arguments:
```bash
ticker -> required stock symbol
days -> optional number of past days of stock price data to fetch (default 31)
```

## Signal Explanations:
```bash
IV Spike: Triggers when today's IV > 1.3× yesterday's
IV vs HV Ratio: Triggers when IV/HV ratio > 1.5 (implied > historical vol)
IV–Price Divergence:  Triggers when IV rises > 10% while stock price stays flat or drops
```


## Project Structure:
```bash
options-volatility-tracker/
├── data/                  # IV and price history + signals.csv
├── logs/                  # Log file
├── src/
│   ├── main.py            # CLI entry point
│   ├── fetch_options.py   # Data fetching (IV, price, HV)
│   ├── signals.py         # All signal logic
│   ├── utils.py           # CSV logging helper
│   └── logger_config.py   # Structured logging config
└── requirements.txt
```

## Technologies Used:
```bash
Python 3
yFinance
Pandas
NumPy
argparse
logging
```

## Author:
```bash
Medha Muskula
Computer Engineering @ UIUC
GitHub: mmedha04
