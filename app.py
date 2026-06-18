import streamlit as st
import ccxt
import pandas as pd

st.set_page_config(page_title="Crypto AI Analyzer", layout="wide")
st.title("📊 AI Crypto Real-Time Analyzer")

@st.cache_data(ttl=60)
def fetch_data(symbol):
    try:
        exchange = ccxt.binance()
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return None

symbol = st.sidebar.selectbox("Pilih Aset", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
df = fetch_data(symbol)

if df is not None:
    # Perhitungan RSI Manual (Tanpa pandas-ta agar aman)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Tampilkan Visual
    st.subheader(f"Data Harga {symbol}")
    st.line_chart(df['close'])

    # Logika Sinyal
    last_rsi = df['RSI'].iloc[-1]
    st.metric("RSI (14) Saat Ini", round(last_rsi, 2))

    if last_rsi < 30:
        st.success("Sinyal: Potensi Kenaikan (Oversold)")
    elif last_rsi > 70:
        st.error("Sinyal: Potensi Penurunan (Overbought)")
    else:
        st.info("Sinyal: Market Sideways / Netral")
else:
    st.warning("Data tidak tersedia saat ini.")
