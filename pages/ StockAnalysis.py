import pandas as pd
import time
import yfinance as yf
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib
import mplfinance as mpf
import warnings
from datetime import date, datetime


st.sidebar.write("""
# 日経225株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示期間選択
""")

start = st.sidebar.date_input(
    "Fromを選択してください。",
    )

st.write("""
### 銘柄選択
""")

filename = 'nikkei.csv'
df = pd.read_csv(filename, encoding='shift-jis')

names = df['銘柄名']

company = st.selectbox(
        '銘柄を選択してください。',
        names,
    )


def get_historical_data(start, company):
    filename = 'nikkei.csv'
    df = pd.read_csv(filename, encoding='shift-jis')

    names = df['銘柄名']

    code = df[df['銘柄名']==company]['コード'].iloc[-1]
    stockCode = str(code) + '.T'
    type(stockCode)

    _df =yf.download(tickers=stockCode, start=start, end=datetime.now())
    date = _df.index

    high = _df['High']
    low = _df['Low']

    max26 = high.rolling(window=26).max()
    min26 = low.rolling(window=26).min()

    _df['basic_line'] = (max26 + min26) / 2

    # 転換線
    high9 = high.rolling(window=9).max()
    low9 = low.rolling(window=9).min()

    _df['turn_line'] = (high9 + low9) / 2
    # 先行スパン1
    
    _df['span1'] = (_df['basic_line'] + _df['turn_line']) / 2

    # 先行スパン2
    high52 = high.rolling(window=52).max()
    low52 = low.rolling(window=52).min()

    _df['span2'] = (high52 + low52) / 2

    # 遅行線
    _df['slow_line'] = _df['Adj Close'].shift(-25)

    return _df

try:
    data = get_historical_data(start, company)
    lines = [mpf.make_addplot(data['basic_line']), # 基準線
            mpf.make_addplot(data['turn_line']), # 転換線
            mpf.make_addplot(data['slow_line']), # 遅行線
            ]

    labels = ['basic', 'turn', 'slow', 'span']

    fig, ax = mpf.plot(data, type='candle', figsize=(16,6),style='yahoo', xrotation=0, addplot=lines, returnfig=True,
                        fill_between=dict(y1=data['span1'].values, y2=data['span2'].values, alpha=0.5, color='gray'))
    ax[0].legend(labels)
    st.pyplot(fig)
except:
    st.error(
        "35日以上の期間を指定してください！"
    )
