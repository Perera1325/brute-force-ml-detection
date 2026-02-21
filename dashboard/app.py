import streamlit as st
import json
import os
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="AI SOC Dashboard",
    layout="wide",
    page_icon="🛡️"
)

# Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# =============================
# Custom CSS (Enterprise Dark)
# =============================

st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.metric-container {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI Intrusion Detection - SOC Dashboard")

SECURITY_PATH = "../security/ip_activity.json"
BLACKLIST_PATH = "../security/blacklist.json"


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


ip_data = load_json(SECURITY_PATH)
blacklist = load_json(BLACKLIST_PATH)

# =============================
# KPI SECTION
# =============================

total_ips = len(ip_data)
total_attacks = sum(ip_data[ip]["attack_count"] for ip in ip_data)
total_requests = sum(len(ip_data[ip].get("timestamps", [])) for ip in ip_data)
total_blacklisted = len(blacklist)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Active IPs", total_ips)
col2.metric("Total Requests", total_requests)
col3.metric("Detected Attacks", total_attacks)
col4.metric("Blacklisted IPs", total_blacklisted)

st.divider()

# =============================
# ATTACK SEVERITY
# =============================

st.subheader("🚨 Threat Level")

if total_attacks > 10:
    st.error("CRITICAL - Active brute force campaign detected!")
elif total_attacks > 3:
    st.warning("MEDIUM - Suspicious activity observed.")
else:
    st.success("LOW - System operating normally.")

st.divider()

# =============================
# IP TABLE
# =============================

st.subheader("📊 IP Activity Overview")

if ip_data:
    table_data = []

    for ip, stats in ip_data.items():
        table_data.append({
            "IP Address": ip,
            "Requests (Window)": len(stats.get("timestamps", [])),
            "Attack Count": stats.get("attack_count", 0),
            "Temp Banned Until": stats.get("banned_until", "None")
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No activity yet.")

st.divider()

# =============================
# ATTACK DISTRIBUTION
# =============================

st.subheader("📈 Attack Distribution")

if ip_data:
    chart_data = {
        ip: stats.get("attack_count", 0)
        for ip, stats in ip_data.items()
    }

    chart_df = pd.DataFrame.from_dict(
        chart_data, orient="index", columns=["Attack Count"]
    )

    st.bar_chart(chart_df)
else:
    st.info("No attack data available.")

st.divider()

# =============================
# BLACKLIST
# =============================

st.subheader("🚫 Blacklisted IPs")

if blacklist:
    blacklist_df = pd.DataFrame.from_dict(
        blacklist, orient="index"
    )
    st.dataframe(blacklist_df, use_container_width=True)
else:
    st.success("No blacklisted IPs.")
