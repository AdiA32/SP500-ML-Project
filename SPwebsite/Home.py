import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="S&P Stock Recommendation System",
    page_icon="📉",
    layout="wide"
)

header=st.container()
stock_drop_down=st.container()
historic_data=st.container()
nlp_twitter=st.container()
nav_bar=st.container()
recommendation=st.container()

with header:
    st.title("S&P Stock Recommendation System 📉")


with stock_drop_down: # actual stock drop-down to be added
    companies=pd.read_csv("data/all_stocks_5yr.csv", delimiter=',')
    names=companies["Name"].unique()
    option = st.selectbox('CHOOSE A STOCK:', (names)) 
    st.write("You selected: ", option)
    st.write(":green[Gives full overview + reccomendation if you scroll]")


with historic_data:
    st.header("Historical Analysis")
    st.write(":green[to do: gives historical analysis for the stock using model+ visualizations]")

with nlp_twitter:
    st.header("Sentiment Analysis")
    st.write(":green[to do: gives sentiment analysis for the stock using nlp model+ visualizations]")

with nav_bar:
    st.sidebar.success("Select an analysis")

with recommendation:
    st.header("Recommendation")
    st.write(":green[Based on the historical and sentiment analysis, gives a yes or no reccomendation]")