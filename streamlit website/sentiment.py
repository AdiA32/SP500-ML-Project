import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from urllib.request import urlopen, Request
from urllib.parse import quote

from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def run_sentiment(tickers: list = ["AMZN", "AAPL"]):
    finviz_url = "https://finviz.com/quote.ashx?t="

    news_tables = {}
    for ticker in tickers:
        url = finviz_url + quote(ticker)

        req = Request(url=url, headers={"user-agent": "my-app"})
        response = urlopen(req)

        html = BeautifulSoup(response, features="html.parser")
        news_table = html.find(id="news-table")
        news_tables[ticker] = news_table

    parsed_data = []

    for ticker, news_table in news_tables.items():
        for row in news_table.findAll("tr"):
            if row.a is None:
                continue
            title = row.a.text
            date_data = row.td.text.split(" ")

            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]

            parsed_data.append([ticker, date, time, title])

    df = pd.DataFrame(parsed_data, columns=["ticker", "date", "time", "title"])

    st.write(df)
    vader = SentimentIntensityAnalyzer()

    f = lambda title: vader.polarity_scores(title)["compound"]
    df["compound"] = df["title"].apply(f)
    df["date"] = pd.to_datetime(df.date).dt.date

    plt.figure(figsize=(10, 8))
    mean_df = df.groupby(["ticker", "date"]).mean().unstack()
    mean_df = mean_df.xs("compound", axis="columns")
    mean_df.plot(kind="bar")
    plt.title("Mean Sentiment Score")
    plt.xlabel("Date")
    plt.ylabel("Compound Sentiment Score")
    st.pyplot(plt)

    # Ensure that the 'date' column is in datetime format
    df["date"] = pd.to_datetime(df["date"])

    # List of unique tickers
    tickers = df["ticker"].unique()

    # Plotting
    for ticker in tickers:
        fig, ax = plt.subplots(figsize=(10, 6))
        df_ticker = df[df["ticker"] == ticker]
        sns.lineplot(
            x="date", y="compound", data=df_ticker, ax=ax, label=ticker
        )

        # Formatting the x-axis as dates
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))

        plt.title(f"Sentiment Trends for {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Compound Sentiment Score")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)


def main():
    st.title("Stock Sentiment Analysis")
    tickers = (
        st.text_input(
            "Enter tickers (comma-separated)",
            value="AMZN, AAPL",
            help="Enter the tickers of the stocks you want to analyze.",
        )
        .upper()
        .split(",")
    )

    st.info("Scraping news data and analyzing sentiment...")
    run_sentiment(tickers)


if __name__ == "__main__":
    main()
