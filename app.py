import streamlit as st
import pandas as pd
import joblib
from log_automation import connect_to_google_sheets, log_to_google_sheet

# Load model and scaler
model = joblib.load("stock_prediction_model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("📈 Algo-Trading System Dashboard")

uploaded_file = st.file_uploader("Upload the latest stock data file (CSV)", type=["csv"])

# Only show Predict button if file is uploaded
if uploaded_file and st.button("Generate Portfolio Analytics"):
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Compute indicators
    df['20_MA'] = df['4. close'].rolling(window=20).mean()
    df['50_MA'] = df['4. close'].rolling(window=50).mean()

    def compute_rsi(data, window=14):
        delta = data['4. close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def compute_macd(data):
        ema_12 = data['4. close'].ewm(span=12, adjust=False).mean()
        ema_26 = data['4. close'].ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal

    df['RSI'] = compute_rsi(df)
    df['MACD'], df['MACD_Signal'] = compute_macd(df)

    features = ['5. volume', '20_MA', '50_MA', 'RSI', 'MACD', 'MACD_Signal']
    df.dropna(inplace=True)
    X_scaled = scaler.transform(df[features])
    predictions = model.predict(X_scaled)

    df['Predicted_Price'] = predictions
    df['Trade_Signal'] = ['Buy' if x > 0.6 else 'Sell' if x < 0.4 else 'Hold' for x in predictions]
    df['P&L'] = df['4. close'].diff().shift(-1) * df['Trade_Signal'].map({'Buy': 1, 'Sell': -1, 'Hold': 0})

    trade_log = df[['4. close', 'Predicted_Price', 'Trade_Signal', 'P&L']].copy()
    total_trades = len(trade_log[trade_log['Trade_Signal'] != 'Hold'])
    win_ratio = len(trade_log[trade_log['P&L'] > 0]) / max(1, total_trades)

    summary = pd.DataFrame({
        'Total Trades': [total_trades],
        'Total P&L': [trade_log['P&L'].sum()],
        'Win Ratio': [win_ratio]
    })

    win_ratio_df = pd.DataFrame({'Win Ratio': [win_ratio]})  # New addition

    # Save to session_state
    st.session_state.trade_log = trade_log
    st.session_state.summary = summary
    st.session_state.win_ratio_df = win_ratio_df  # New addition

    st.dataframe(trade_log.head(50))
    st.dataframe(summary)

# Display if session state is populated (to persist across reruns)
if "trade_log" in st.session_state and "summary" in st.session_state:
    st.subheader("📊 Last Trade Log")
    st.dataframe(st.session_state.trade_log.tail(20))

    st.subheader("📈 P&L Summary")
    st.dataframe(st.session_state.summary)

    if st.button("Log to Google Sheets"):
        try:
            trade_log = st.session_state.trade_log.replace([float('inf'), float('-inf')], pd.NA).dropna()
            summary = st.session_state.summary.replace([float('inf'), float('-inf')], pd.NA).dropna()
            win_ratio_df = st.session_state.win_ratio_df.replace([float('inf'), float('-inf')], pd.NA).dropna()  # New addition

            sheet = connect_to_google_sheets("Trade_Logs")
            log_to_google_sheet(sheet, trade_log, "Trade Log")
            log_to_google_sheet(sheet, summary, "P&L Summary")
            log_to_google_sheet(sheet, win_ratio_df, "Win Ratio")  
            st.success("✅ Trade log, summary, and win ratio successfully logged to Google Sheets.")
        except Exception as e:
            st.error(f"Logging failed: {e}")
