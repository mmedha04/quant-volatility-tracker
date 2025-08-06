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
    
    