import pandas as pd 
import numpy as np 

def calculate_sma(df, short_window=7, long_window=50):
    df['Short_SMA'] = df['Close'].rolling(window=short_window).mean()
    df['Long_SMA'] = df['Close'].rolling(window=long_window).mean()
    return df


