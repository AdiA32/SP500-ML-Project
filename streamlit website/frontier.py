import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime as dt
import yfinance as yfin
import scipy.optimize as sc
import plotly.graph_objects as go
import streamlit as st

yfin.pdr_override()

def getData(stocks, start, end):
    stockData = pdr.get_data_yahoo(stocks, start=start, end=end)
    stockData = stockData["Close"]
    return stockData.pct_change()

def portfolioPerformance(weights, meanReturns, covMatrix):
    returns = np.sum(meanReturns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights))) * np.sqrt(252)
    return returns, std

def random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate):
    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolioPerformance(weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_std_dev
        results[1, i] = portfolio_return
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record

def display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate):
    results, weights = random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx], index=mean_returns.index, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx], index=mean_returns.index, columns=['allocation'])
    min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    st.write("-" * 80)
    st.write("Maximum Sharpe Ratio Portfolio Allocation")
    st.write("Annualised Return:", round(rp, 2))
    st.write("Annualised Volatility:", round(sdp, 2))
    st.write(max_sharpe_allocation)
    st.write("-" * 80)
    st.write("Minimum Volatility Portfolio Allocation")
    st.write("Annualised Return:", round(rp_min, 2))
    st.write("Annualised Volatility:", round(sdp_min, 2))
    st.write(min_vol_allocation)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=results[0, :],
            y=results[1, :],
            mode="markers",
            marker=dict(
                size=10,
                color=results[2, :],
                colorscale="Viridis",
                showscale=True
            ),
            text=[f"Return: {round(rp*100, 2)}%, Volatility: {round(sdp*100, 2)}%" for rp, sdp in zip(results[1, :], results[0, :])]
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[sdp],
            y=[rp],
            mode="markers",
            marker=dict(
                size=12,
                color="red",
                symbol="star"
            ),
            name="Maximum Sharpe Ratio"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[sdp_min],
            y=[rp_min],
            mode="markers",
            marker=dict(
                size=12,
                color="green",
                symbol="star"
            ),
            name="Minimum Volatility"
        )
    )
    fig.update_layout(
        title="Simulated Portfolio Optimization based on Efficient Frontier",
        xaxis=dict(title="Annualised Volatility"),
        yaxis=dict(title="Annualised Return"),
        showlegend=True,
        legend=dict(x=0.75, y=0, traceorder="normal", bgcolor="#E2E2E2", bordercolor="black", borderwidth=2),
        width=800,
        height=600
    )
    st.plotly_chart(fig)

def main():
    st.title("Portfolio Optimization with Efficient Frontier")
    stock_list = st.text_input("Enter Stock Tickers (comma-separated)", "AAPL,AMZN,GOOGL,META").upper().split(",")
    risk_free_rate = st.number_input("Risk-Free Rate", value=0.0178, step=0.0001)
    num_portfolios = st.number_input("Number of Portfolios to Simulate", value=25000, step=1000)

    start_date = dt.datetime.now() - dt.timedelta(days=365)
    end_date = dt.datetime.now()
    pctChange = getData(stock_list, start_date, end_date)

    mean_returns = pctChange.mean()
    cov_matrix = pctChange.cov()

    if st.button("Run Analysis"):
        st.info("Running Portfolio Optimization Analysis")
        display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate)

if __name__ == "__main__":
    main()
