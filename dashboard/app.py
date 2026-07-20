import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Medicare Advantage Dashboard",
    layout="wide"
)

st.title("Medicare Advantage Geographic Variation Dashboard")

st.write(
    "This dashboard uses CMS public Medicare Advantage Geographic Variation data "
    "to explore enrollment, demographics, and utilization by state."
)

# File paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data_processed" / "ma_geo_state_2022_analysis.csv"

# Load data
df = pd.read_csv(DATA_PATH)

# Sidebar filters
years = sorted(df["YEAR"].dropna().unique())
selected_year = st.sidebar.selectbox(
    "Select year",
    years,
    index=len(years) - 1
)

df_year = df[df["YEAR"] == selected_year].copy()

st.subheader(f"Overview - {selected_year}")

# KPI cards
total_ma_benes = df_year["BENES_MA_CNT"].sum()
avg_age = df_year["BENE_AVG_AGE"].mean()
avg_er_visits = df_year["ER_VISITS_PER_1000_BENES"].mean()
avg_op_visits = df_year["OP_VISITS_PER_1000_BENES"].mean()
num_states = df_year["STATE"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("MA Beneficiaries", f"{total_ma_benes:,.0f}")
col2.metric("States", f"{num_states}")
col3.metric("Average Age", f"{avg_age:.1f}")
col4.metric("ER Visits / 1,000", f"{avg_er_visits:.1f}")
col5.metric("OP Visits / 1,000", f"{avg_op_visits:.1f}")

st.divider()

# Top 10 MA enrollment
st.subheader("Top 10 States by Medicare Advantage Beneficiaries")

top10_benes = df_year.sort_values(
    "BENES_MA_CNT",
    ascending=False
).head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(top10_benes["STATE"], top10_benes["BENES_MA_CNT"])
ax1.set_title(f"Top 10 States by Medicare Advantage Beneficiaries, {selected_year}")
ax1.set_xlabel("State")
ax1.set_ylabel("Medicare Advantage Beneficiaries")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

st.dataframe(
    top10_benes[
        [
            "STATE",
            "BENES_MA_CNT",
            "BENE_AVG_AGE",
            "BENE_DUAL_PCT",
            "ER_VISITS_PER_1000_BENES",
            "OP_VISITS_PER_1000_BENES",
        ]
    ],
    use_container_width=True,
)

st.divider()

# Top 10 ER visits
st.subheader("Top 10 States by ER Visits per 1,000 MA Beneficiaries")

top10_er = df_year.sort_values(
    "ER_VISITS_PER_1000_BENES",
    ascending=False
).head(10)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(top10_er["STATE"], top10_er["ER_VISITS_PER_1000_BENES"])
ax2.set_title(f"Top 10 States by ER Visits per 1,000 MA Beneficiaries, {selected_year}")
ax2.set_xlabel("State")
ax2.set_ylabel("ER Visits per 1,000 Beneficiaries")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

st.dataframe(
    top10_er[
        [
            "STATE",
            "BENES_MA_CNT",
            "ER_VISITS_PER_1000_BENES",
            "OP_VISITS_PER_1000_BENES",
        ]
    ],
    use_container_width=True,
)

st.divider()

# Full data table
st.subheader("State-Level Data")

st.dataframe(df_year, use_container_width=True)

csv = df_year.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name=f"ma_geo_state_{selected_year}.csv",
    mime="text/csv",
)
