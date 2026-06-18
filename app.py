import streamlit as st
import yfinance as yf # Mengganti ccxt dengan yfinance

st.title("📊 Crypto Analyzer")

symbol = st.sidebar.selectbox("Pilih Aset", ["BTC-USD", "ETH-USD", "SOL-USD"])

@st.cache_data(ttl=60)
def fetch_data(symbol):
    # Mengambil data dari Yahoo Finance (tidak diblokir lokasi)
    df = yf.download(symbol, period="1d", interval="1h")
    return df

df = fetch_data(symbol)

if not df.empty:
    st.line_chart(df['Close'])
    # Logika RSI manual tetap bisa digunakan di sini...
else:
    st.write("Data tidak ditemukan.")
