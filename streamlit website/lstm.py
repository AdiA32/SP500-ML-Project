import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import plotly.express as px


def lstm_stock_prediction(ticker):
    start = dt.datetime.now() - dt.timedelta(days=(4 * 365))
    end = dt.datetime.now()
    df = yf.Ticker(ticker).history(start=start, end=end)
    df = df.iloc[:, :-2]
    st.write(df)
    st.write("We chose our target variable to be the 'Opening Price', represented by the column 'Open'")

    training_set = df.iloc[:, 1:2].values
    sc = MinMaxScaler()
    training_set = sc.fit_transform(training_set)

    X_train = training_set[0:1005]
    y_train = training_set[1:1006]
    X_train = np.reshape(X_train, (X_train.shape[0], 1, 1))

    regressor = Sequential()
    regressor.add(LSTM(units=4, activation="sigmoid", input_shape=(None, 1)))
    regressor.add(Dense(1))
    regressor.compile(loss="mean_squared_error", optimizer="adam")
    regressor.summary()
    regressor.fit(X_train, y_train, batch_size=32, epochs=200)

    test_start = end - dt.timedelta(days=30)
    test_df = yf.Ticker(ticker).history(start=test_start, end=end)
    test_df = test_df.iloc[:, :-2]
    test_set = test_df.iloc[:-1, 1:2].values
    test_inputs = sc.transform(test_set)
    test_inputs = np.reshape(test_inputs, (test_inputs.shape[0], 1, 1))

    predicted_price = regressor.predict(test_inputs)
    predicted_price = sc.inverse_transform(predicted_price)

    # Adjust the predicted prices to match the length of test_df
    predicted_price = np.concatenate((np.zeros((1, 1)), predicted_price))
    predicted_price = np.squeeze(predicted_price)

    test_df["Predictions"] = predicted_price
    test_df["Error"] = test_df["Predictions"] - test_df["Open"]

    test_df = test_df.reset_index()  # Reset index to make "Date" a column
    test_df["Date"] = test_df["Date"] + pd.DateOffset(days=2)  # Offset the starting date by one day
    st.plotly_chart(px.line(test_df, x="Date", y=["Open", "Predictions"], labels={"value": "Price", "variable": "Type"}))


def main():
    st.title("Stock Price Prediction using LSTM")
    ticker = st.text_input("Enter Stock Ticker Symbol (e.g., GOOGL, AAPL)", "GOOGL")
    if st.button("Run Analysis"):
        st.info("Running LSTM analysis for stock: " + ticker)
        lstm_stock_prediction(ticker)


if __name__ == "__main__":
    main()
