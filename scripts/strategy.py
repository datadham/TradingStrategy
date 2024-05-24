import pandas as pd 
import numpy as np 


def generate_sma_signals(df):
        df['Buy'] = np.where((df['Short_SMA'] > df['Long_SMA']) & (df['Short_SMA'].shift(1) <= df['Long_SMA'].shift(1)), 1, 0)
        df['Sell'] = np.where((df['Short_SMA'] < df['Long_SMA']) & (df['Short_SMA'].shift(1) >= df['Long_SMA'].shift(1)), -1, 0)
        return df


def apply_strategy(df):
        df = df.reset_index()
        # When you have the signal you buy at the price of the day after
        df['day_after'] = df['Date'].shift(-1)
        df['buy_price'] = df['Open'].shift(-1)
        
        holding = False
        trade = {}
        trades = []

        for i, row in df.iterrows():
            if row['Buy'] == 1 and not holding:
                holding = True
                trade = {
                    'entry_date': row['day_after'],
                    'entry_price': row['buy_price']
                }

            if holding and row['Sell'] == -1:
                holding = False
                trade['exit_date'] = row['day_after']
                trade['exit_price'] = row['buy_price']
                trades.append(trade)
                trade = {}
        return df, trades

def performance_df(trades):
    if trades.empty:
        return pd.DataFrame()
    
    # Convert date columns to datetime
    trades['exit_date'] = pd.to_datetime(trades['exit_date'])
    trades['entry_date'] = pd.to_datetime(trades['entry_date'])

    # Calculate returns for each trade
    trades['return'] = (trades['exit_price'] - trades['entry_price']) / trades['entry_price']
    trades['holding_time'] = (trades['exit_date'] - trades['entry_date']).dt.days

    # Calculate performance metrics
    win_rate = (trades['return'] > 0).mean()
    cum_return = (1 + trades['return']).prod() - 1
    std_dev = trades['return'].std()
    sharpe_ratio = trades['return'].mean() / trades['return'].std() * np.sqrt(len(trades))
    buy_and_hold_return = (trades['exit_price'].iloc[-1] - trades['entry_price'].iloc[0]) / trades['entry_price'].iloc[0]
    avg_holding_time = trades['holding_time'].mean()

    # Calculate maximum drawdown
    trades['cumulative_return'] = (1 + trades['return']).cumprod()
    cumulative_max = trades['cumulative_return'].cummax()
    drawdown = (trades['cumulative_return'] - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()

    # Report performance
    performance_report = pd.DataFrame({
        'Metric': ['Win Rate', 'Standard Deviation', 'Sharpe Ratio', 'Buy and Hold Return', 'Cumulative Return', 'Average Holding Time', 'Max Drawdown'],
        'Value': [win_rate, std_dev, sharpe_ratio, buy_and_hold_return, cum_return, avg_holding_time, max_drawdown]
    })

    return performance_report