import streamlit as st
import pandas as pd
from utils.parser import get_all_usage_data
import os

st.set_page_config(page_title="OpenClaw Usage Dashboard", layout="wide")

st.title("💰 OpenClaw Token Usage Dashboard")
st.markdown("Real-time monitoring of your AI assistant's costs.")

# Configuration
SESSIONS_DIR = os.path.expanduser("~/.openclaw/agents/main/sessions/")

# Fetch data
with st.spinner("Analyzing session logs..."):
    data = get_all_usage_data(SESSIONS_DIR)
    df = pd.DataFrame(data)

if not df.empty:
    # Summary Metrics
    total_in = df['input_tokens'].sum()
    total_out = df['output_tokens'].sum()
    # Estimate cost (Gemini 1.5 Flash rates: $0.075/1M in, $0.30/1M out as of early 2025/2026 approximation)
    est_cost = (total_in / 1_000_000 * 0.075) + (total_out / 1_000_000 * 0.30)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Input Tokens", f"{total_in:,}")
    col2.metric("Total Output Tokens", f"{total_out:,}")
    col3.metric("Estimated Cost (USD)", f"${est_cost:.4f}")

    st.subheader("📊 Usage by Session File")
    st.dataframe(df.sort_values(by="last_updated", ascending=False), use_container_width=True)

    # Simple bar chart
    st.subheader("Token Distribution")
    st.bar_chart(df.set_index('file')[['input_tokens', 'output_tokens']])
else:
    st.warning("No session logs found in the directory.")

st.sidebar.info(f"Monitoring directory: {SESSIONS_DIR}")
