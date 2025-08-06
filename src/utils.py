import pandas as pd
import os

def log_signal_to_csv(date, ticker, signal_type, message, path = "../data/signals.csv"):
    # make sure path exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    #create a data frame for new row
    new_row = pd.DataFrame([{
        "date" : str(date),
        "ticker": ticker, 
        "signal_type": signal_type,
        "message": message
    }])

    #append or create new file
    if os.path.exists(path):
        new_row.to_csv(path, mode = "a", header = False, index = False)
    else:
        new_row.to_csv(path, index=False)

