#the main file to run all functions
from fetch_options import fetch_stock_data, fetch_iv_data, compute_hv
from signals import detect_iv_spike, detect_iv_vs_hv
from datetime import datetime #gives you current date & time
import os #use to check if a file exists or if we need to create a new one
import pandas as pd
import argparse #used for creating command line interfaces (CLI)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Options Volatility Tracker") #initialize parser
    parser.add_argument("--ticker", type=str, required=True, help= "Stock ticker symbol, ex:AAPL")
    parser.add_argument("--days", type=int, default=31, help= "Number of days for historical data")
    args = parser.parse_args()

    symbol = args.ticker.upper() #gets user input signal
    days = args.days #gets user input days if user chose to

    today = datetime.now().date() #get current date
    print(f"\nRunning analysis for {symbol} on {today}...")

    #get price data & IV
    price_data = fetch_stock_data(symbol, period=f"{days}d")
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
    

    #Market signal 1: IV Spike Detection
    spike_check, spike_msg = detect_iv_spike(iv_yesterday, iv_today, symbol)
    print(spike_msg)

    #Market Signal 2: IV vs HV Detection
    hv_today = compute_hv(price_data)
    ratio_check, ratio_msg = detect_iv_vs_hv(hv_today, iv_today, symbol)
    print(ratio_msg)
    


    

    
