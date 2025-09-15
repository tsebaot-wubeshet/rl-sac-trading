import yfinance as yf
import pandas as pd

def get_gold_data():
    gold = yf.Ticker("GC=F")
    # fetch historical data by 1d interval
    data1 = gold.history(start = "2010-01-01", end = "2015-12-31", interval = "1d")
    data2 = gold.history(start = "2016-01-01", end = "2020-12-31", interval = "1d")
    data3 = gold.history(start = "2021-01-01", end = "2024-12-31", interval = "1d")

    data_2010_2020 = pd.concat([data1, data2])
    data_2021_2025 = data3

    data_2010_2020.to_csv("./historical_data/2010_2020_gold.csv")
    data_2021_2025.to_csv("./historical_data/2021_2025_gold.csv")

    print(f"Data saved! {data3.tail()}")
    

get_gold_data()