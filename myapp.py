import streamlit as st
import yfinance as yf
from phishing.phishing_fast import check_phishing_rule
from blockchain.blockchain_utils import save_log, get_all_logs
import time
import pandas as pd

st.set_page_config(page_title="HDBank Demo", layout="wide")

menu = st.sidebar.radio("Choose:", ["🏦 Chatbot Advisor", "🛡️ Phishing Detector", "🔗 Blockchain Log"])

# Helper: supported tickers
valid_tickers = {
    "google":"GOOGL","apple":"AAPL","tesla":"TSLA","amazon":"AMZN","microsoft":"MSFT"
}

# ---------------- Chatbot Advisor tab ----------------
if menu == "🏦 Chatbot Advisor":
    st.title("💬 AI Financial Advisor (Demo)")
    st.write("You can ask: 'google', 'apple price', 'tesla volume', or 'apple and tesla'")

    time_range = st.selectbox("Select time range", ["1d","5d","1mo","6mo","1y"], index=4)
    user_input = st.text_input("Your question:")

    if st.button("Send"):
        # find tickers
        ticks = []
        for name,sym in valid_tickers.items():
            if name in user_input.lower():
                ticks.append((name,sym))
        if not ticks:
            st.info("Supported: " + ", ".join(valid_tickers.keys()))
        else:
            for name,symbol in ticks:
                st.subheader(f"{name.title()} ({symbol})")
                t = yf.Ticker(symbol)
                if time_range == "1d":
                    df = t.history(period="1d", interval="5m")
                else:
                    df = t.history(period=time_range)
                # show price + volume by default
                st.write("📈 Closing Price")
                st.line_chart(df.Close)
                st.write("📊 Volume")
                st.line_chart(df.Volume)

                # summary
                info = t.info
                cp = info.get("currentPrice")
                prev = info.get("previousClose")
                if cp and prev:
                    change = (cp - prev)/prev*100
                    st.write(f"Current price: {cp}  |  Change: {change:.2f}%")
                    if change > 5:
                        st.error("🚨 Price surged >5%")
                    if change < -5:
                        st.warning("⚠️ Price dropped >5%")
                # save to blockchain (shorten data)
                try:
                    short = f"{name}:{user_input[:120]}"
                    tx = save_log("advice", short)
                    st.write("Saved to blockchain tx:", tx)
                except Exception as e:
                    st.write("Blockchain save failed:", e)

# ---------------- Phishing Detector tab ----------------
elif menu == "🛡️ Phishing Detector":
    st.title("🛡️ Phishing Email/SMS Detector")
    sample = st.text_area("Paste email/SMS here:")
    if st.button("Check"):
        res = check_phishing_rule(sample)
        if res["label"] == "phishing":
            st.error(f"⚠️ Phishing detected (score {res['score']})")
        else:
            st.success(f"✅ Safe (score {res['score']})")
        st.write("Reasons:", res["reasons"])
        # save event
        try:
            short = (sample[:140] + "...") if len(sample) > 140 else sample
            tx = save_log("phishing", short)
            st.write("Saved to blockchain tx:", tx)
        except Exception as e:
            st.write("Blockchain save failed:", e)

# ---------------- Blockchain Log tab ----------------
elif menu == "🔗 Blockchain Log":
    st.title("🔗 Blockchain Audit Log")
    try:
        logs = get_all_logs()
        if logs:
            df = pd.DataFrame(logs)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            st.dataframe(df)
        else:
            st.info("No logs yet.")
    except Exception as e:
        st.write("Cannot read logs:", e)
        st.write("Make sure Ganache is running and contract deployed.")
