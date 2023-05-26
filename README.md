# SP500-ML-Project
Introduction:  
The purpose of this project is to optimize stock portfolio allocation using a blend of machine learning, sentiment analysis, and portfolio optimization techniques. We first utilize LSTM models to forecast movements in a pool of stocks, alongside sentiment analysis derived from relevant Twitter and news data. The aim is to predict whether a given stock's price will ascend or descend. We then take the recommended stocks from these LSTM and sentiment analyses and feed them into an Efficient Frontier model. This model computes the optimal balance of these stocks in a portfolio to maximize return for a given level of risk. By integrating time-series forecasting, natural language processing, and portfolio theory, we hope to provide more comprehensive and potentially profitable stock portfolio recommendations than with purely numerical analysis, considering the wider sentiment landscape surrounding each stock.

Problems: 
1) Efficient Market Hypothesis - Random Walk
2) Non Stationarity: While it is possible for Stock Prices to be viewed as time-series data, we have to realize that price movements across time are Non-Stationary. This means that the distribution (mean and variance) of the data set changes over time. This makes it very difficult to develop a prediction model that is accurate and usable across any extended time period as the distribution of our training and testing data are very different.
3) Difficult to predict effects of future events - Pandemics, Wars, Politics , Elections 
4) Too many correlated features to feed into Machine Learning models, 
5) NLP not always predictive, users ≠ stock owners

Data Cleaning: 

PREDICTION MODELS: (most important part) 

LSTM: LSTM (Long Short-Term Memory) is a type of recurrent neural network (RNN) that can effectively capture sequential patterns in data. In the context of stock prediction, you can use historical stock price data to train an LSTM model to learn patterns and trends

How we selected it: 
Most normal Recurrent Neural Networks (RNNs) face the challenge of not being able to capture ‘long-term dependencies’ in their models. We want to incorporate historical stock price data, over a long time period, into our model so that we can predict future Opening Price. LSTMs are useful in that they can enhance the modeling of long-term dependencies by incorporating memory cells and gating mechanisms, LSTMs can selectively 'remember' or 'forget' information, enabling them to capture and utilize long-range dependencies in sequential data.

Why: 
Stock Prices suffer from the problem of Non-Stationarity across time periods. LSTM helps overcome the non-stationarity issue in stock prices, as it doesn't rely on a specific time period or distribution. It incorporates patterns across a lengthy timeframe, thus encompassing diverse distributions.

Pros/Cons: LSTM addresses data non-stationarity and offers decent accuracy. However, it doesn't address the Random Walk Hypothesis, limiting its prediction capacity. Furthermore, historical price, in general, isn't a strong predictor of future price, limiting its real-world applicability in areas like hedge funds or quantitative analysis.

Results:
The LSTM model predicted the direction of Google's [GOOGL] opening price movements with reasonable accuracy, albeit overpredicting by an average of $3.04 per day, with a maximum error of $6.





Sentiment Analysis Using NLP:

For our project, we initially attempted to leverage Twitter data to derive sentiment around given stocks using tools such as Twint and Snscrape. However, due to policy changes at Twitter, these tools became obsolete, necessitating a pivot in our strategy.

We are now utilizing the limited Twitter API directly to scrape relevant tweets, supplemented with sentiment from popular news outlets. The sentiment is derived through two NLP models:

1. VADER: A rule-based sentiment analysis tool. Strengths include simplicity, ease of interpretation, and low computational resource requirements. However, it struggles with complex sentences and sarcasm.

2. BERT (current): A transformer-based NLP technique pre-trained and then fine-tuned for sentiment analysis. Strengths include the understanding of context in sentences, which makes it powerful for handling complex and ambiguous language. Its limitations include the need for substantial computational resources and data for fine-tuning.

In terms of merging the sentiments derived from Twitter and news sources, we are using a weighted aggregation approach, accounting for factors such as the recency and relevance of the information. The final output is a composite sentiment score that will be used alongside the LSTM model to make predictions. 


RECOMMENDATION MODEL:

Overcoming the Efficient Markets Problem:
Since we know that Stock prices cannot be predicted consistently using only historical price movements, we make use of Modern Portfolio Theory to find a way to recommend Stocks to include in your portfolio without relying only Predicted Price.  

Instead of ‘Predicted Price’ we focus on 2 Parameters: Return and Risk. 

Portfolio Return is defined as the weighted average of Returns of all stocks in a given portfolio

Portfolio Risk refers to the potential for the actual returns of a portfolio to deviate from the expected or desired returns.It is measured as the weighted average of the standard deviation of the Portfolio of stocks

An Optimal Portfolio - Minimizes  Risk & Maximises Returns. 

GRAPHING THE EFFICIENT FRONTIER: 

The Efficient Frontier graphically illustrates the optimal portfolio combinations that achieve the highest expected return for a given level of risk or the lowest level of risk for a given expected return. The x-axis represents the standard deviation or volatility, which is a measure of the portfolio's risk, while the y-axis represents the expected return.

Once we predict the performance of a given stock using our Predictive Models (LSTM, Twitter Sentiment) we feed the best performing stocks into our Efficient Frontier Model and that graphs the optimal set of Portfolios involving these stocks and presents the optimal ratio of stocks in the portfolio.






Results: 
<need to include sample portfolio> 
 

Future Steps: 
1. Enhanced Sentiment Analysis: Include more data sources, refine NLP for financial language.
2. Deep Learning Models: Explore use of CNNs or transformer models for stock predictions.
3. Portfolio Optimization Methods: Investigate advanced models considering transaction costs, taxes.
4. Real-time Application: Develop a tool for real-time portfolio recommendations.
5. Model Interpretability: Increase transparency in decision-making process.
6. Backtesting and Performance Metrics: Backtest models with historical data, establish performance metrics.
