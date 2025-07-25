#fetch options data
#this code will dowload stock price history, fetch current IV from options chains, and save the data in csv & print avg IV
import yfinance as yf 
import pandas as pd
import numpy as np
from datetime import datetime #gives you current date & time
import os #use to check if a file exists or if we need to create a new one

#  gets daily stock prices for the last 31 days for the given ticker_symbol

def fetch_stock_data(ticker_symbol, period='31d', interval='1d'): #we can use AMZN to test
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period, interval=interval) #history returns DataFrame w columns
    return hist

#fetch IV from options data
def fetch_iv_data(ticker_symbol, num_expirations=2, pct_range=0.05): #2 means it gets next 2 expirations, 0.05 is percentage range from curr price for ntm
    ticker = yf.Ticker(ticker_symbol)
    expirations = ticker.options[:num_expirations] #holds list of expiration dates for the options

    ivs = [] #implied volatilities
    for exp in expirations: #looking at next expirations, get option contracts that expire on those days(calls and puts)
        current_price = ticker.history(period="1d")["Close"].iloc[-1] #curr is price of stock from today's close
        chain = ticker.option_chain(exp) #fetches option chain -> table of calls and puts for a stock on certain date

        #filter for near the money calls and puts, this makes iv accurate more estimate, basically filtering out outliers
        
        calls_ntm = chain.calls[(chain.calls.strike >= current_price * (1 - pct_range)) & #strike is the action you do when u buy/sell
                                (chain.calls.strike <= current_price * (1 + pct_range))]
        
        puts_ntm = chain.puts[(chain.puts.strike >= current_price * (1 - pct_range)) &
                                (chain.puts.strike <= current_price * (1 + pct_range))]
        
        ivs += list(calls_ntm.impliedVolatility.dropna()) 
        ivs += list(puts_ntm.impliedVolatility.dropna()) #dropna to skip contracts w/o IV

        if ivs:
            return pd.Series(ivs).mean() 
        else:
            None

    
# compute historical volatility from past stock price data
def compute_hv(price_data, window=20): #window is num of past days we are calculating from
    # Ensure 'Close' column exists and has enough data
    if "Close" not in price_data.columns:
        print("Error: 'Close' column not found in price data.")
        return None
    if len(price_data) < window:
        print(f" Not enough data to compute {window}-day HV. Only {len(price_data)} rows available.")
        return None
   
    price_data = price_data.copy() #make copy of price_data for this function to use
    price_data["log_return"] = np.log(price_data["Close"] / price_data["Close"].shift(1)) #calculates log return for window # of days

     # Rolling standard deviation of log returns used to calculate hv
    price_data["hv"] = price_data["log_return"].rolling(window).std()
    
    # return most recent hv value thats not null, if all null, return none
    hv = price_data["hv"].dropna()
    if hv.empty:
        print("HV calculation resulted in all NaNs.")
        return None

    return hv.iloc[-1]

if __name__ == "__main__":
    symbol = "AAPL" #testing using amazon options data
    today = datetime.now().date() #get current date
    print(f"\nRunning analysis for {symbol} on {today}...")

    #get price data & IV
    price_data = fetch_stock_data(symbol)
    iv_today = fetch_iv_data(symbol)

    if iv_today is None: #if no iv data, leave main
        print(f"No valid IV data found for {symbol}. Skipping.")
        exit()

    #save stock prices
    price_data.to_csv(f"../data/{symbol}_price.csv")
    #path to save iv history
    iv_path = f"../data/{symbol}_iv_history.csv"

    iv_yesterday = None
    iv_logged_today = False

    #load existing iv data if it exists
    if os.path.exists(iv_path): #if we alr saved data
        iv_hist = pd.read_csv(iv_path) #just read the data thats already been saved
        
        # If today's IV is already logged
        if str(today) in iv_hist["date"].values:
            print(f"✅ {symbol}: IV for {today} already logged. Skipping entry.")
            iv_logged_today = True
            iv_yesterday = iv_hist.iloc[-1]["iv"]
        else:
            iv_yesterday = iv_hist.iloc[-1]["iv"]
            new_row = pd.DataFrame([{"date": today, "iv": iv_today}])
            new_row.to_csv(iv_path, mode="a", header=False, index=False)
    
    else:
        print(f"🆕 First run — saving today's IV for {symbol}.")
        new_row = pd.DataFrame([{"date": today, "iv": iv_today}])
        new_row.to_csv(iv_path, index=False)
    
    # Market Signal 1: IV Spike
    if iv_yesterday != None:
        if iv_today > iv_yesterday * 1.3:
            print(f"🚨 {symbol}: IV spiked {(iv_today / iv_yesterday - 1) * 100:.2f}%!") # dif signifcant bc more than 30%
        else:
            print(f"{symbol}: No major IV spike.")
    
   # Market Signal 2: IV vs HV ratio
    hv_today = compute_hv(price_data)
    iv_hv_ratio = iv_today/hv_today
    
    print(f"IV = {iv_today:.4f}, HV = {hv_today:.4f}, IV/HV = {iv_hv_ratio:.2f}")
    if iv_hv_ratio > 1.5:
        print(f"🚨 {symbol}: IV > 1.5 * HV — Market expects more movement than reality.")
    

    

    
