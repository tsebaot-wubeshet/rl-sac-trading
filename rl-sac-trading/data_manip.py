import pandas as pd
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator
from ta.trend import MACD
from pyts.image import GramianAngularField

from common import logMessage
import numpy as np

def prep():
    d1 = pd.read_csv("./historical_data/2010_2020_gold.csv", index_col="Date", parse_dates=True)
    d2 = pd.read_csv("./historical_data/2021_2025_gold.csv", index_col="Date", parse_dates=True)

    df = pd.concat([d1, d2]).sort_index()
    df = df.dropna()
    df = df[~df.index.duplicated(keep='first')]

    logMessage(f"Prepared data : {df.tail()}")

    return df

def indicators(df):

    df['ATR'] = AverageTrueRange(df['High'], df['Low'], df['Close'], window=14).average_true_range()
    df['RSI'] = RSIIndicator(df['Close'], window=14).rsi()
    macd = MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
    df['MACD'] = macd.macd_diff()

    logMessage(f" ATR: {df['ATR']}, RSI: {df['RSI']}, MACD: {df['MACD']}")

    for col in ['ATR', 'RSI', 'MACD']:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) # normalize values

    logMessage(f"Normalized data : {df.tail()}")

    return df

def gaf(df):
    gaf = GramianAngularField(image_size=24, method='summation')
    window_size = 24
    gaf_images = []
    gaf_indices = []

    close_series = df['Close'].values

    for i in range(window_size, len(close_series)):
        window = close_series[i - window_size:i]
        normalized = (window - np.min(window)) / (np.max(window) - np.min(window))
        gaf_image = gaf.fit_transform(normalized.reshape(1, -1))[0]
        gaf_images.append(gaf_image)
        gaf_indices.append(df.index[i])

    return gaf_images, gaf_indices