import twint
import pandas as pd
import re

def get_stock_tweets(stock_ticker, num_tweets):
    # Configuring twint search
    c = twint.Config()
    c.Search = stock_ticker
    c.Lang = 'en'
    c.Limit = num_tweets
    c.Pandas = True

    # Running search
    twint.run.Search(c)

    # Getting a pandas DataFrame of tweets
    tweets_df = twint.storage.panda.Tweets_df
    
    return tweets_df

def filter_tweets(df, stock_ticker):
    # Define other tickers pattern
    other_tickers = re.compile(r'\$[a-zA-z]+')

    # Exclude tweets with other tickers, links, and possible chatroom messages
    df_filtered = df[~df['tweet'].str.contains('|'.join(['http', 'https', 'discord', 'chat', 'room']))]
    df_filtered = df[df['tweet'].apply(lambda x: len(re.findall(other_tickers, x)) <= 1)]

    return df_filtered

def store_tweets(df, stock_ticker):
    # Store the data to csv
    df.to_csv(f'{stock_ticker}_tweets.csv', index=False)

# Use the functions
stock_ticker = '$AAPL' # or any ticker
num_tweets = 1000 # or any number of tweets
df = get_stock_tweets(stock_ticker, num_tweets)
df_filtered = filter_tweets(df, stock_ticker)
store_tweets(df_filtered, stock_ticker)
