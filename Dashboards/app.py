import streamlit as st
import sqlite3
import pandas as pd
import time

st.set_page_config(page_title="SentinelFlow", layout="wide")
st.title("SentinelFlow — Live Network Anomaly Dashboard")

DB_PATH = "/app/api/alerts.db"

def load_alerts():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM alerts ORDER BY id DESC LIMIT 100", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Could not read alerts.db: {e}")
        return pd.DataFrame()

placeholder = st.empty()

while True:
    df = load_alerts()
    with placeholder.container():
        if df.empty:
            st.info("No alerts yet — waiting for traffic...")
        else:
            st.metric("Total Alerts", len(df))
            st.dataframe(df, use_container_width=True)
    time.sleep(3)
