from unicodedata import name
import pandas as pd
import time
import yfinance as yf
import altair as alt
import streamlit as st
# import matplotlib.pyplot as plt
# import japanize_matplotlib
import mplfinance as mpf
import warnings
from datetime import date, datetime

st.title("日経225株価可視化アプリ")

st.write("""
    こちらは株価可視化ツールです。
    日経225の銘柄比較と銘柄の一目均衡表を確認することができます。
""")

filename = 'nikkei.csv'
df = pd.read_csv(filename, encoding='shift-jis')

col1, col2 = st.columns(2)
with col1:
    st.write("""
    ### 日経225銘柄一覧
    """)
    st.dataframe(df, 800, 500)

with col2:
    st.write("""
    ### アプリの説明
    """)
    st.write("""
    「StockAnalysis」では、銘柄の一目均衡表を表示します。株価変動の分析にお役立てください。

    「StockCompare」では銘柄の株価比較ができます。同業種の銘柄比較などに役立てください。

    表示される図はダウンロードできるので、ご自由にお使いください。
    """)
