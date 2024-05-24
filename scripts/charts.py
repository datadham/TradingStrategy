import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def showtrades(hist,trades, Close, annot=False):
    fig = px.line(hist, x='Date', y="Close")
    for i, row in trades.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['entry_date'], row['exit_date']],
            y=[row['entry_price'], row['exit_price']],
            mode='lines+markers',
            line=dict(color='green' if row['exit_price'] > row['entry_price'] else 'red'),
            marker=dict(size=10),
            name=f'Trade {i+1}'
        ))
    fig.add_scatter(x=trades['entry_date'], y=trades['entry_price'], mode='markers', name='Entry Points', marker=dict(color='blue', size=10))
    fig.add_scatter(x=trades['exit_date'], y=trades['exit_price'], mode='markers', name='Exit Points', marker=dict(color='purple', size=10))
    
    for i, row in trades.iterrows():
            fig.add_annotation(
                x=row['entry_date'],
                y=row['entry_price'],
                text=f'{int(row["entry_price"])}',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-20,
                font=dict(color='blue')
            )
            fig.add_annotation(
                x=row['exit_date'],
                y=row['exit_price'],
                text=f'{int(row["exit_price"])}',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-20,
                font=dict(color='purple')
            )
    return fig