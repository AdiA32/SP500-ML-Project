import streamlit as st
from sentiment import run_sentiment
import lstm
import frontier


def main():
    st.title("Stock Sentiment Analysis")
    tickers = st.text_input(
        "Enter tickers (comma-separated)",
        value="AMZN, AAPL",
        help="Enter the tickers of the stocks you want to analyze.",
    ).upper().split(",")

    st.info("Scraping news data and analyzing sentiment...")
    run_sentiment(tickers)


if __name__ == "__main__":
    main()
