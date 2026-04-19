"""
app.py — Streamlit Interactive Dashboard
-----------------------------------------
Run:  streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

from data_generator import generate_expenses
from analysis import (
    clean_data, summary_stats, category_analysis,
    monthly_trends, payment_analysis, quarterly_analysis,
    budget_analysis, top_transactions, detect_anomalies, savings_estimate,
)

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💸 Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Dark theme CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .stMetric { background: #1a1a2e; border-radius: 10px; padding: 10px; }
    h1,h2,h3 { color: #e0e0e0 !important; }
    .stDataFrame { background: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

BG    = "#0f0f1a"
CARD  = "#1a1a2e"
GRID  = "#2a2a3e"
TEXT  = "#e0e0e0"
ACC   = "#7c3aed"

CAT_COLORS = {
    "Food & Dining":"#f97316","Rent":"#ef4444","Transportation":"#3b82f6",
    "Entertainment":"#a855f7","Utilities":"#06b6d4","Healthcare":"#22c55e",
    "Shopping":"#ec4899","Education":"#eab308","Travel":"#14b8a6",
    "Subscriptions":"#8b5cf6","Groceries":"#84cc16","Personal Care":"#fb923c",
}

# ─── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    if os.path.exists("data/expenses.csv"):
        df = pd.read_csv("data/expenses.csv", parse_dates=["date"])
    else:
        df = generate_expenses()
    return clean_data(df)

df_full = load_data()

# ─── Sidebar filters ─────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")

months = sorted(df_full["month_num"].unique())
month_names = df_full.sort_values("month_num")[["month_num","month"]].drop_duplicates()
month_map   = dict(zip(month_names["month_num"], month_names["month"]))

selected_months = st.sidebar.multiselect(
    "Month",
    options=months,
    default=months,
    format_func=lambda x: month_map[x]
)

all_cats = sorted(df_full["category"].unique())
selected_cats = st.sidebar.multiselect("Category", options=all_cats, default=all_cats)
monthly_income = st.sidebar.number_input("Monthly Income (₹)", value=60000, step=5000)

df = df_full[
    df_full["month_num"].isin(selected_months) &
    df_full["category"].isin(selected_cats)
]

# ─── Title ────────────────────────────────────────────────────────────────────
st.title("💸 Expense Tracker Dashboard — 2024")
st.markdown("**Synthetic Data · Data Science Project · Python + Streamlit**")
st.divider()

# ─── KPI Cards ───────────────────────────────────────────────────────────────
stats   = summary_stats(df)
savings = savings_estimate(df, monthly_income * len(selected_months))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Total Spent",       f"₹{stats['total_spent']:,.0f}")
c2.metric("📋 Transactions",      stats['total_transactions'])
c3.metric("📊 Avg Transaction",   f"₹{stats['avg_transaction']:,.0f}")
c4.metric("📈 Max Transaction",   f"₹{stats['max_transaction']:,.0f}")
c5.metric("💵 Savings Rate",      f"{savings['savings_rate_pct']:.1f}%")

st.divider()

# ─── Row 1: Pie + Monthly Trend ──────────────────────────────────────────────
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🍕 Spending by Category")
    cat_df = category_analysis(df)
    fig, ax = plt.subplots(figsize=(6, 5), facecolor=BG)
    ax.set_facecolor(BG)
    colors = [CAT_COLORS.get(c, "#888") for c in cat_df["category"]]
    wedges, _, autotexts = ax.pie(
        cat_df["total"], labels=None, colors=colors,
        autopct="%1.1f%%", startangle=140, pctdistance=0.75,
        wedgeprops=dict(edgecolor=BG, linewidth=2)
    )
    for at in autotexts:
        at.set_color("white"); at.set_fontsize(7)
    ax.legend(wedges, cat_df["category"], loc="center left",
              bbox_to_anchor=(1, 0.5), fontsize=7, frameon=False, labelcolor=TEXT)
    st.pyplot(fig)

with col2:
    st.subheader("📈 Monthly Spending Trend")
    monthly_df = monthly_trends(df)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=BG)
    ax.set_facecolor(CARD)
    x = range(len(monthly_df))
    ax.fill_between(x, monthly_df["total"], alpha=0.18, color=ACC)
    ax.plot(x, monthly_df["total"], color=ACC, linewidth=2.5,
            marker="o", markersize=6, markerfacecolor="white")
    ax.set_xticks(list(x))
    ax.set_xticklabels([m[:3] for m in monthly_df["month"]], color=TEXT, fontsize=8)
    ax.tick_params(colors=TEXT)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"₹{v/1000:.0f}K"))
    for sp in ["top","right"]: ax.spines[sp].set_visible(False)
    for sp in ["bottom","left"]: ax.spines[sp].set_color(GRID)
    ax.yaxis.grid(True, color=GRID, linestyle="--", alpha=0.4)
    ax.set_facecolor(CARD)
    st.pyplot(fig)

# ─── Row 2: Bar chart + Payment methods ──────────────────────────────────────
col3, col4 = st.columns([1.5, 1])

with col3:
    st.subheader("📊 Category-wise Spending")
    fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
    ax.set_facecolor(CARD)
    colors = [CAT_COLORS.get(c, "#888") for c in cat_df["category"]]
    ax.barh(cat_df["category"], cat_df["total"], color=colors, edgecolor="none", height=0.6)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"₹{v/1000:.0f}K"))
    ax.tick_params(colors=TEXT, labelsize=8)
    for sp in ["top","right"]: ax.spines[sp].set_visible(False)
    for sp in ["bottom","left"]: ax.spines[sp].set_color(GRID)
    ax.yaxis.grid(False); ax.xaxis.grid(True, color=GRID, linestyle="--", alpha=0.4)
    st.pyplot(fig)

with col4:
    st.subheader("💳 Payment Methods")
    pay_df = payment_analysis(df)
    fig, ax = plt.subplots(figsize=(5, 5), facecolor=BG)
    ax.set_facecolor(BG)
    pcols = ["#7c3aed","#3b82f6","#22c55e","#f97316","#ec4899"]
    wedges, texts, ats = ax.pie(
        pay_df["total"], labels=None, colors=pcols[:len(pay_df)],
        autopct="%1.1f%%", startangle=90, pctdistance=0.75,
        wedgeprops=dict(edgecolor=BG, linewidth=2)
    )
    for at in ats: at.set_color("white"); at.set_fontsize(8)
    ax.legend(wedges, pay_df["payment_method"], loc="lower center",
              bbox_to_anchor=(0.5,-0.15), ncol=3, fontsize=7,
              frameon=False, labelcolor=TEXT)
    st.pyplot(fig)

# ─── Row 3: Budget vs Actual ─────────────────────────────────────────────────
st.subheader("🎯 Budget vs Actual Monthly Spend")
budget_df = budget_analysis(df)
fig, ax = plt.subplots(figsize=(14, 4), facecolor=BG)
ax.set_facecolor(CARD)
cats   = budget_df["category"].tolist()
actual = budget_df["actual_monthly_avg"].tolist()
budget = budget_df["budget"].tolist()
x4     = np.arange(len(cats))
w      = 0.35
ax.bar(x4 - w/2, budget, w, label="Budget", color="#3b82f6", edgecolor="none", alpha=0.8)
ax.bar(x4 + w/2, actual, w, label="Actual",
       color=[("#ef4444" if a > b else "#22c55e") for a,b in zip(actual,budget)],
       edgecolor="none", alpha=0.8)
ax.set_xticks(x4)
ax.set_xticklabels(cats, rotation=20, ha="right", fontsize=8, color=TEXT)
ax.tick_params(colors=TEXT)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"₹{v/1000:.0f}K"))
ax.legend(frameon=False, labelcolor=TEXT, fontsize=9)
for sp in ["top","right"]: ax.spines[sp].set_visible(False)
for sp in ["bottom","left"]: ax.spines[sp].set_color(GRID)
ax.yaxis.grid(True, color=GRID, linestyle="--", alpha=0.4)
st.pyplot(fig)

# ─── Row 4: Tables ───────────────────────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("🏆 Top 10 Transactions")
    top_df = top_transactions(df, 10)
    st.dataframe(
        top_df[["date","category","description","amount","payment_method"]]
        .rename(columns={"payment_method":"Payment"}),
        use_container_width=True, height=300
    )

with col6:
    st.subheader("🚨 Anomalies Detected")
    anom = detect_anomalies(df)
    if len(anom):
        st.dataframe(
            anom[["date","category","description","amount","z_score"]].head(10),
            use_container_width=True, height=300
        )
    else:
        st.info("No anomalies detected in the selected data.")

# ─── Row 5: Insights ─────────────────────────────────────────────────────────
st.subheader("🔍 Key Insights")
from insights import generate_insights
insights = generate_insights(stats, cat_df, monthly_df, budget_df, anom, savings)
for ins in insights:
    st.markdown(f"- {ins}")

st.divider()
st.caption("Built with 🐍 Python · Pandas · Matplotlib · Streamlit  |  Synthetic Data — 2024")
