import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Multi-Crypto Predictor", layout="wide")
st.title("📈 Multi-Crypto Potential Predictor")

# Daftar koin yang ingin dipantau
assets = ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "DOGE-USD"]

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

st.write("Analisis berdasarkan indikator RSI (14 periode):")

for asset in assets:
    df = yf.download(asset, period="5d", interval="1h", progress=False)
    if not df.empty:
        df['RSI'] = calculate_rsi(df)
        current_rsi = df['RSI'].iloc[-1]
        
        col1, col2 = st.columns([1, 2])
        col1.subheader(asset)
        
        if current_rsi < 30:
            col2.success(f"RSI: {current_rsi:.2f} | Potensi: **UPTREND** (Oversold)")
        elif current_rsi > 70:
            col2.error(f"RSI: {current_rsi:.2f} | Potensi: **DOWNTREND** (Overbought)")
        else:
            col2.info(f"RSI: {current_rsi:.2f} | Potensi: **NETRAL**")
    else:
        st.write(f"Data {asset} tidak tersedia.")
