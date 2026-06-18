
    import streamlit as st
    import ccxt
    import pandas as pd
    import pandas_ta as ta

    st.title("Crypto AI")
    
    # Ambil data
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=50)
    df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
    
    # Hitung RSI
    df['RSI'] = ta.rsi(df['close'], length=14)
    
    # Tampil di Web
    st.line_chart(df['close'])
    st.write(f"RSI Saat Ini: {df['RSI'].iloc[-
