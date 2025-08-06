#use this for detecting signals such as iv spikes 
from fetch_options import fetch_stock_data, fetch_iv_data, compute_hv

def detect_iv_spike(iv_yesterday, iv_today, symbol, threshold=1.3):
    # Market Signal 1: IV Spike
    #this function detects significant iv spikes compared to the previous day
    if iv_yesterday != None and iv_today != None:
        if iv_today > iv_yesterday * threshold:
            percent_change = ((iv_today / iv_yesterday) - 1) * 100
            return True, f"🚨 {symbol}: IV spiked {percent_change:.2f}%!" # dif signifcant bc more than 30%, :.2f means to 2 decimal places
        else:
            return False, f"{symbol}: No major IV spike."
    else:
        return False, f"{symbol}: Missing IV data."

    
def detect_iv_vs_hv(hv_today, iv_today, symbol, threshold=1.5):
    # Market Signal 2: IV vs HV ratio
    # this function compares current iv to historical volatitilty (hv) ratio
    if hv_today is None or iv_today is None or hv_today == 0:
        return False, f"{symbol}: Missing valid HV/IV data."
    iv_hv_ratio = iv_today/hv_today
    
    result = f"IV = {iv_today:.4f}, HV = {hv_today:.4f}, IV/HV = {iv_hv_ratio:.2f}"
    if iv_hv_ratio > threshold:
        return True, f"🚨 {symbol}: IV > 1.5 * HV — Market expects more movement than reality."

    return False, result
    
#when IV rises while the stock price stays flat or drops, it could indicate market nervousness or an upcoming move
def detect_iv_price_divergence(iv_today, iv_yesterday, price_data, symbol, threshold=0.1):
    #this function detects divergence when IV increases and price does not.
    if iv_yesterday is None or iv_today is None:
        return False, f"{symbol}: Missing valid IV data."

    if len(price_data) < 2: #dont have past 2 days data
        return False, f"{symbol}: Lacking price data for divergence check."
    
    iv_change = (iv_today - iv_yesterday) / iv_yesterday
    price_today = price_data["Close"].iloc[-1]
    price_yesterday = price_data["Close"].iloc[-2]
    price_change = (price_today - price_yesterday) / price_yesterday

    if iv_change > threshold and price_change <= 0:
        return True, f"🚨{symbol}: IV raised {iv_change:.2%} while price fell {price_change:.2%} -> Divergence detected."
    else:
        return False, f"{symbol}: IV change = {iv_change:.2%}, Price change = {price_change:.2%} — No divergence."

    #use past 2-day price change and current IV change
    #if IV increases by 10% while price is flat or down -> flag it
    #print + log the signal in main.py
    