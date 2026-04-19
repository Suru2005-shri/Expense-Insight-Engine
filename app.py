"""
╔══════════════════════════════════════════════════════════╗
║   DYNAMIC EXPENSE TRACKER — Real-time User Data Entry    ║
║   Run:  streamlit run app.py                             ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io
import os
from datetime import datetime, date

# ══════════════════════════════════════════════════════════════
#  CONFIG & CONSTANTS
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE   = "data/user_expenses.csv"
BUDGET_FILE = "data/user_budgets.csv"
os.makedirs("data", exist_ok=True)

CATEGORIES = [
    "Food & Dining", "Rent", "Transportation", "Entertainment",
    "Utilities", "Healthcare", "Shopping", "Education",
    "Travel", "Subscriptions", "Groceries", "Personal Care", "Other",
]

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

CAT_COLORS = {
    "Food & Dining":  "#f97316", "Rent":           "#ef4444",
    "Transportation": "#3b82f6", "Entertainment":  "#a855f7",
    "Utilities":      "#06b6d4", "Healthcare":     "#22c55e",
    "Shopping":       "#ec4899", "Education":      "#eab308",
    "Travel":         "#14b8a6", "Subscriptions":  "#8b5cf6",
    "Groceries":      "#84cc16", "Personal Care":  "#fb923c",
    "Other":          "#94a3b8",
}

BG, CARD, GRID, TEXT, ACC = "#0d0d1a", "#161628", "#252540", "#e2e8f0", "#6366f1"

DEFAULT_BUDGETS = {
    "Food & Dining": 5000, "Rent": 12000, "Transportation": 3000,
    "Entertainment": 4000, "Utilities": 3000, "Healthcare": 3000,
    "Shopping": 5000, "Education": 8000, "Travel": 10000,
    "Subscriptions": 1500, "Groceries": 6000, "Personal Care": 2000,
    "Other": 2000,
}

MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0d0d1a;
    color: #e2e8f0;
}
.stApp { background-color: #0d0d1a; }

section[data-testid="stSidebar"] {
    background: #0a0a14 !important;
    border-right: 1px solid #252540;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important;
     font-size: 2rem !important; letter-spacing: -0.03em;
     background: linear-gradient(135deg, #6366f1, #a78bfa, #06b6d4);
     -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
h2, h3 { font-family: 'Syne', sans-serif !important;
          font-weight: 700 !important; color: #e2e8f0 !important; }

[data-testid="metric-container"] {
    background: #161628; border: 1px solid #252540;
    border-radius: 12px; padding: 16px !important;
    transition: border-color .2s;
}
[data-testid="metric-container"]:hover { border-color: #6366f1; }
[data-testid="stMetricValue"] { color: #a78bfa !important;
    font-size: 1.6rem !important; font-weight: 500 !important; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.75rem !important; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input,
.stTextArea textarea {
    background: #1e1e38 !important;
    border: 1px solid #252540 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important; padding: 0.5rem 1.5rem !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(99,102,241,.4) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #161628; border-radius: 10px;
    padding: 4px; gap: 4px; border: 1px solid #252540;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #94a3b8 !important;
    border-radius: 8px !important; font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    background: #252540 !important; color: #a78bfa !important;
}

hr { border-color: #252540 !important; margin: 1.5rem 0; }

.stSuccess { background: #0d2e1a !important;
    border-left: 3px solid #22c55e !important; border-radius: 8px !important; }
.stWarning { background: #2e1f0d !important;
    border-left: 3px solid #f97316 !important; border-radius: 8px !important; }
.stError   { background: #2e0d0d !important;
    border-left: 3px solid #ef4444 !important; border-radius: 8px !important; }
.stInfo    { background: #0d1a2e !important;
    border-left: 3px solid #6366f1 !important; border-radius: 8px !important; }

.streamlit-expanderHeader {
    background: #161628 !important; border: 1px solid #252540 !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
}
.streamlit-expanderContent {
    background: #161628 !important; border: 1px solid #252540 !important;
    border-top: none !important; border-radius: 0 0 8px 8px !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg,#6366f1,#a78bfa) !important; border-radius: 4px;
}

.insight-row {
    background: #1e1e38; border-left: 3px solid #6366f1;
    border-radius: 0 8px 8px 0; padding: .6rem 1rem;
    margin: .4rem 0; font-size: .85rem;
}

.improve-card {
    background: linear-gradient(135deg, #1e1e38, #161628);
    border: 1px solid #252540; border-radius: 12px;
    padding: 1.2rem 1.5rem; margin: .6rem 0;
    transition: border-color .2s, transform .2s;
}
.improve-card:hover { border-color:#6366f1; transform:translateX(4px); }
.improve-card h4 { margin:0 0 .4rem 0; color:#a78bfa; font-size:.9rem; }
.improve-card p  { margin:0; color:#94a3b8; font-size:.8rem; line-height:1.6; }

.tag { display:inline-block; padding:2px 10px; border-radius:999px;
       font-size:.72rem; font-weight:500; letter-spacing:.05em; }
.tag-over  { background:#2e0d0d; color:#ef4444; border:1px solid #ef4444; }
.tag-under { background:#0d2e1a; color:#22c55e; border:1px solid #22c55e; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  DATA PERSISTENCE
# ══════════════════════════════════════════════════════════════

def load_expenses() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, parse_dates=["date"])
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
            if "note" not in df.columns:
                df["note"] = ""
            return df
        except Exception:
            pass
    return pd.DataFrame(columns=["id","date","category","description",
                                  "amount","payment_method","note"])

def save_expenses(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)

def load_budgets() -> dict:
    if os.path.exists(BUDGET_FILE):
        try:
            b = pd.read_csv(BUDGET_FILE)
            return dict(zip(b["category"], b["budget"]))
        except Exception:
            pass
    return DEFAULT_BUDGETS.copy()

def save_budgets(budgets: dict):
    pd.DataFrame(list(budgets.items()),
                 columns=["category","budget"]).to_csv(BUDGET_FILE, index=False)

def next_id(df: pd.DataFrame) -> str:
    if df.empty:
        return "EXP0001"
    try:
        nums = df["id"].str.extract(r"(\d+)")[0].astype(int)
        return f"EXP{(nums.max()+1):04d}"
    except Exception:
        return f"EXP{len(df)+1:04d}"

# Init session state
if "df" not in st.session_state:
    st.session_state.df = load_expenses()
if "budgets" not in st.session_state:
    st.session_state.budgets = load_budgets()
if "show_budget_modal" not in st.session_state:
    st.session_state.show_budget_modal = False
if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False


# ══════════════════════════════════════════════════════════════
#  CHART HELPERS
# ══════════════════════════════════════════════════════════════

def _fig(w, h):
    return plt.figure(figsize=(w, h), facecolor=BG)

def _ax(fig, pos=111):
    ax = fig.add_subplot(pos)
    ax.set_facecolor(CARD)
    for sp in ["top","right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["bottom","left"]:
        ax.spines[sp].set_color(GRID)
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.yaxis.grid(True, color=GRID, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    return ax

def rupee_fmt(ax, axis="y"):
    fmt = mticker.FuncFormatter(
        lambda v,_: f"Rs.{v/1000:.0f}K" if v >= 1000 else f"Rs.{v:.0f}"
    )
    if axis == "y": ax.yaxis.set_major_formatter(fmt)
    else:           ax.xaxis.set_major_formatter(fmt)

def show(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight", facecolor=BG)
    buf.seek(0)
    st.image(buf, use_column_width=True)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════
#  ANALYSIS HELPERS
# ══════════════════════════════════════════════════════════════

def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"]        = pd.to_datetime(df["date"])
    df["month"]       = df["date"].dt.strftime("%B")
    df["month_num"]   = df["date"].dt.month
    df["year"]        = df["date"].dt.year
    df["day_of_week"] = df["date"].dt.strftime("%A")
    df["quarter"]     = df["date"].dt.quarter.map(lambda q: f"Q{q}")
    return df

def kpis(df):
    if df.empty:
        return {}
    return {
        "total":      df["amount"].sum(),
        "count":      len(df),
        "avg":        df["amount"].mean(),
        "max":        df["amount"].max(),
        "categories": df["category"].nunique(),
        "date_from":  df["date"].min().strftime("%d %b %Y"),
        "date_to":    df["date"].max().strftime("%d %b %Y"),
    }

def detect_anomalies(df, z=2.5):
    if len(df) < 5:
        return pd.DataFrame()
    df2 = df.copy()
    df2["z"] = df2.groupby("category")["amount"].transform(
        lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0
    )
    return df2[df2["z"] > z].sort_values("z", ascending=False)


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ExpenseTracker")
    st.markdown("---")

    df_all   = st.session_state.df
    total_amt = df_all["amount"].sum() if not df_all.empty else 0
    total_txn = len(df_all)

    st.markdown(f"""
    <div style='background:#1e1e38;border-radius:10px;padding:12px 16px;margin-bottom:1rem;'>
      <div style='color:#94a3b8;font-size:.7rem;'>TOTAL LOGGED</div>
      <div style='color:#a78bfa;font-size:1.4rem;font-weight:500;'>Rs.{total_amt:,.0f}</div>
      <div style='color:#64748b;font-size:.72rem;'>{total_txn} transactions</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Filters")
    df_e = enrich(df_all) if not df_all.empty else pd.DataFrame()

    years = sorted(df_e["year"].unique().tolist()) if not df_e.empty else [datetime.now().year]
    sel_year = st.selectbox("Year", ["All"] + [str(y) for y in years])

    cats_avail = sorted(df_e["category"].unique().tolist()) if not df_e.empty else CATEGORIES
    sel_cats   = st.multiselect("Categories", cats_avail, default=cats_avail)

    months_avail = sorted(df_e["month_num"].unique().tolist()) if not df_e.empty else list(range(1,13))
    sel_months   = st.multiselect(
        "Months", months_avail, default=months_avail,
        format_func=lambda m: MONTH_ORDER[m-1]
    )

    st.markdown("---")
    st.markdown("### Income & Budget")
    monthly_income = st.number_input("Monthly Income (Rs.)", value=60000, step=5000, min_value=0)

    if st.button("Manage Category Budgets", use_container_width=True):
        st.session_state.show_budget_modal = not st.session_state.show_budget_modal

    st.markdown("---")

    if not df_all.empty:
        csv_bytes = df_all.to_csv(index=False).encode()
        st.download_button(
            "Download My Data (CSV)",
            data=csv_bytes, file_name="my_expenses.csv",
            mime="text/csv", use_container_width=True,
        )

    if st.button("Clear All Data", use_container_width=True):
        st.session_state.confirm_clear = True


# Apply filters
df_f = enrich(df_all) if not df_all.empty else pd.DataFrame()
if not df_f.empty:
    if sel_year != "All":
        df_f = df_f[df_f["year"] == int(sel_year)]
    if sel_cats:
        df_f = df_f[df_f["category"].isin(sel_cats)]
    if sel_months:
        df_f = df_f[df_f["month_num"].isin(sel_months)]


# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════

st.markdown("# Expense Tracker")
st.markdown(
    "<p style='color:#64748b;font-size:.85rem;margin-top:-.5rem;'>"
    "Enter your expenses — get instant analysis, charts & insights</p>",
    unsafe_allow_html=True
)
st.markdown("---")


# ══════════════════════════════════════════════════════════════
#  CONFIRM CLEAR
# ══════════════════════════════════════════════════════════════

if st.session_state.confirm_clear:
    st.error("This will delete ALL your expense data. Are you sure?")
    cc1, cc2, _ = st.columns([1,1,4])
    with cc1:
        if st.button("Yes, Delete"):
            st.session_state.df = pd.DataFrame(
                columns=["id","date","category","description","amount","payment_method","note"]
            )
            save_expenses(st.session_state.df)
            st.session_state.confirm_clear = False
            st.rerun()
    with cc2:
        if st.button("Cancel"):
            st.session_state.confirm_clear = False
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  BUDGET MANAGER
# ══════════════════════════════════════════════════════════════

if st.session_state.show_budget_modal:
    with st.expander("Set Monthly Budgets per Category", expanded=True):
        budgets = st.session_state.budgets
        cols_b  = st.columns(3)
        new_budgets = {}
        for i, cat in enumerate(CATEGORIES):
            with cols_b[i % 3]:
                val = st.number_input(
                    cat,
                    value=int(budgets.get(cat, DEFAULT_BUDGETS.get(cat, 2000))),
                    step=500, min_value=0, key=f"bud_{cat}"
                )
                new_budgets[cat] = val
        bc1, bc2 = st.columns([1,5])
        with bc1:
            if st.button("Save Budgets"):
                st.session_state.budgets = new_budgets
                save_budgets(new_budgets)
                st.session_state.show_budget_modal = False
                st.success("Budgets saved!")
                st.rerun()
        with bc2:
            if st.button("Close Panel"):
                st.session_state.show_budget_modal = False
                st.rerun()


# ══════════════════════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  Add Expense  ",
    "  Dashboard  ",
    "  My Expenses  ",
    "  Budget  ",
    "  Insights  ",
])


# ══════════════════════════════════════════════════════════════
#  TAB 1 — ADD EXPENSE
# ══════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### Add a New Expense")
    m1, m2 = st.tabs(["  Manual Entry  ", "  Upload CSV  "])

    with m1:
        with st.form("add_expense_form", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                exp_date   = st.date_input("Date", value=date.today())
                exp_cat    = st.selectbox("Category", CATEGORIES)
                exp_amount = st.number_input("Amount (Rs.)", min_value=0.0,
                                              step=10.0, format="%.2f")
            with fc2:
                exp_desc    = st.text_input("Description",
                                             placeholder="e.g. Zomato Order, Uber Ride")
                exp_payment = st.selectbox("Payment Method", PAYMENT_METHODS)
                exp_note    = st.text_area("Note (optional)", height=95,
                                            placeholder="Any extra info...")

            submitted = st.form_submit_button("Add Expense", use_container_width=True)
            if submitted:
                if exp_amount <= 0:
                    st.error("Amount must be greater than 0.")
                elif not exp_desc.strip():
                    st.error("Please enter a description.")
                else:
                    new_row = pd.DataFrame([{
                        "id":             next_id(st.session_state.df),
                        "date":           pd.Timestamp(exp_date),
                        "category":       exp_cat,
                        "description":    exp_desc.strip(),
                        "amount":         round(exp_amount, 2),
                        "payment_method": exp_payment,
                        "note":           exp_note.strip(),
                    }])
                    st.session_state.df = pd.concat(
                        [st.session_state.df, new_row], ignore_index=True
                    )
                    save_expenses(st.session_state.df)
                    st.success(
                        f"Added: {exp_desc} — Rs.{exp_amount:,.2f} [{exp_cat}]"
                    )
                    st.balloons()

    with m2:
        st.markdown("#### Upload a CSV File")
        st.markdown("Required columns: `date, category, description, amount, payment_method`")
        st.markdown("Optional: `note`")

        st.markdown("**Sample format:**")
        sample = pd.DataFrame([
            {"date":"2024-01-15","category":"Food & Dining",
             "description":"Zomato Order","amount":450,"payment_method":"UPI","note":""},
            {"date":"2024-01-20","category":"Transportation",
             "description":"Uber Ride","amount":180,"payment_method":"Credit Card","note":"Late night"},
        ])
        st.dataframe(sample, use_container_width=True, hide_index=True)

        uploaded = st.file_uploader("Choose CSV", type=["csv"])
        if uploaded:
            try:
                udf = pd.read_csv(uploaded)
                udf.columns = [c.strip().lower().replace(" ","_") for c in udf.columns]
                required = {"date","category","description","amount","payment_method"}
                missing  = required - set(udf.columns)
                if missing:
                    st.error(f"Missing columns: {missing}")
                else:
                    udf["date"]   = pd.to_datetime(udf["date"], errors="coerce")
                    udf["amount"] = pd.to_numeric(udf["amount"], errors="coerce").fillna(0)
                    udf["note"]   = udf["note"].fillna("") if "note" in udf.columns else ""
                    udf = udf.dropna(subset=["date"])
                    udf["category"] = udf["category"].where(
                        udf["category"].isin(CATEGORIES), other="Other"
                    )
                    udf["payment_method"] = udf["payment_method"].where(
                        udf["payment_method"].isin(PAYMENT_METHODS), other="UPI"
                    )
                    st.markdown(f"**Preview ({len(udf)} rows):**")
                    st.dataframe(udf.head(5), use_container_width=True, hide_index=True)
                    if st.button(f"Import {len(udf)} Rows"):
                        ids = [f"EXP{(len(st.session_state.df)+i+1):04d}"
                               for i in range(len(udf))]
                        udf.insert(0, "id", ids)
                        st.session_state.df = pd.concat(
                            [st.session_state.df, udf], ignore_index=True
                        )
                        save_expenses(st.session_state.df)
                        st.success(f"Imported {len(udf)} expenses!")
                        st.rerun()
            except Exception as e:
                st.error(f"Error reading file: {e}")

    if not st.session_state.df.empty:
        st.markdown("---")
        st.markdown("#### Recently Added (last 5)")
        recent = st.session_state.df.tail(5).iloc[::-1].copy()
        recent["date"]   = pd.to_datetime(recent["date"]).dt.strftime("%d %b %Y")
        recent["amount"] = recent["amount"].map(lambda x: f"Rs.{x:,.2f}")
        st.dataframe(
            recent[["id","date","category","description","amount","payment_method"]],
            use_container_width=True, hide_index=True
        )


# ══════════════════════════════════════════════════════════════
#  TAB 2 — DASHBOARD
# ══════════════════════════════════════════════════════════════

with tab2:
    if df_f.empty:
        st.info("No data yet. Go to Add Expense to get started!")
    else:
        k = kpis(df_f)

        # KPIs
        k1,k2,k3,k4,k5 = st.columns(5)
        k1.metric("Total Spent",    f"Rs.{k['total']:,.0f}")
        k2.metric("Transactions",   k['count'])
        k3.metric("Avg per Txn",    f"Rs.{k['avg']:,.0f}")
        k4.metric("Largest Txn",    f"Rs.{k['max']:,.0f}")
        k5.metric("Categories",     k['categories'])

        months_n     = max(df_f["month_num"].nunique(), 1)
        savings_rate = ((monthly_income - k["total"]/months_n) / monthly_income * 100) \
                       if monthly_income else 0
        sr_color = "#22c55e" if savings_rate>=20 else "#f97316" if savings_rate>=0 else "#ef4444"
        st.markdown(
            f"<div style='text-align:right;color:{sr_color};font-size:.85rem;'>"
            f"Est. savings rate: <b>{savings_rate:.1f}%</b></div>",
            unsafe_allow_html=True
        )
        st.markdown("---")

        # Row 1: Pie + Monthly Trend
        r1c1, r1c2 = st.columns([1,1.6])

        with r1c1:
            st.markdown("#### Category Split")
            cat_grp = df_f.groupby("category")["amount"].sum().sort_values(ascending=False)
            fig = _fig(6,5)
            ax  = fig.add_subplot(111)
            ax.set_facecolor(BG)
            colors = [CAT_COLORS.get(c,"#888") for c in cat_grp.index]
            wedges,_,ats = ax.pie(
                cat_grp.values, labels=None, colors=colors,
                autopct="%1.1f%%", startangle=140, pctdistance=0.78,
                wedgeprops=dict(edgecolor=BG, linewidth=2)
            )
            for at in ats:
                at.set_color("white"); at.set_fontsize(7.5)
            ax.legend(wedges, cat_grp.index, loc="center left",
                      bbox_to_anchor=(1,.5), fontsize=7, frameon=False, labelcolor=TEXT)
            show(fig)

        with r1c2:
            st.markdown("#### Monthly Spending Trend")
            mgrp = (df_f.groupby(["month_num","month"])["amount"]
                    .sum().reset_index().sort_values("month_num"))
            if len(mgrp) >= 2:
                fig = _fig(9,5)
                ax  = _ax(fig)
                x   = range(len(mgrp))
                ax.fill_between(x, mgrp["amount"], alpha=0.12, color=ACC)
                ax.plot(x, mgrp["amount"], color=ACC, linewidth=2.5,
                        marker="o", markersize=7, markerfacecolor="white",
                        markeredgecolor=ACC, markeredgewidth=2)
                for xi,(_,row) in enumerate(mgrp.iterrows()):
                    ax.annotate(f"Rs.{row['amount']/1000:.1f}K",
                                xy=(xi,row["amount"]), xytext=(0,12),
                                textcoords="offset points", ha="center",
                                color=TEXT, fontsize=7.5)
                ax.set_xticks(list(x))
                ax.set_xticklabels([m[:3] for m in mgrp["month"]], color=TEXT, fontsize=9)
                rupee_fmt(ax)
                show(fig)
            else:
                st.info("Add expenses across multiple months to see the trend chart.")

        # Row 2: Category bar + Payment pie
        r2c1, r2c2 = st.columns([1.6,1])

        with r2c1:
            st.markdown("#### Spending by Category")
            cat_grp2 = df_f.groupby("category")["amount"].sum().sort_values()
            fig = _fig(9,5)
            ax  = _ax(fig)
            colors2 = [CAT_COLORS.get(c,"#888") for c in cat_grp2.index]
            bars = ax.barh(cat_grp2.index, cat_grp2.values,
                           color=colors2, edgecolor="none", height=0.6)
            for bar,val in zip(bars, cat_grp2.values):
                ax.text(bar.get_width() + max(cat_grp2.values)*.01,
                        bar.get_y()+bar.get_height()/2,
                        f"Rs.{val:,.0f}", va="center", color=TEXT, fontsize=7.5)
            rupee_fmt(ax,"x")
            ax.yaxis.grid(False)
            ax.xaxis.grid(True, color=GRID, linestyle="--", alpha=0.4)
            show(fig)

        with r2c2:
            st.markdown("#### Payment Methods")
            pay_grp = df_f.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
            fig = _fig(5,5)
            ax  = fig.add_subplot(111)
            ax.set_facecolor(BG)
            pcols = ["#6366f1","#3b82f6","#22c55e","#f97316","#ec4899"]
            ax.pie(pay_grp.values, labels=None, colors=pcols[:len(pay_grp)],
                   autopct="%1.1f%%", startangle=90, pctdistance=0.75,
                   wedgeprops=dict(edgecolor=BG, linewidth=2))
            ax.legend(pay_grp.index, loc="lower center", bbox_to_anchor=(.5,-.1),
                      ncol=3, fontsize=7, frameon=False, labelcolor=TEXT)
            show(fig)

        # Monthly stacked bar
        if df_f["month_num"].nunique() >= 2:
            st.markdown("#### Monthly Breakdown by Category")
            pivot = df_f.pivot_table(
                index="month_num", columns="category",
                values="amount", aggfunc="sum", fill_value=0
            )
            pivot.index = [MONTH_ORDER[m-1][:3] for m in pivot.index]
            fig = _fig(14,5)
            ax  = _ax(fig)
            colors_stk = [CAT_COLORS.get(c,"#888") for c in pivot.columns]
            pivot.plot(kind="bar", stacked=True, ax=ax,
                       color=colors_stk, edgecolor="none", width=0.6)
            ax.set_xticklabels(pivot.index, rotation=0, color=TEXT, fontsize=9)
            rupee_fmt(ax)
            ax.legend(loc="upper left", bbox_to_anchor=(1,1),
                      fontsize=7, frameon=False, labelcolor=TEXT)
            show(fig)

        # Day-of-week chart
        st.markdown("#### Avg Spend by Day of Week")
        dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow = (df_f.groupby("day_of_week")["amount"].mean()
               .reindex(dow_order).fillna(0))
        fig = _fig(10,4)
        ax  = _ax(fig)
        bar_cols = [ACC if d in ("Saturday","Sunday") else "#334155" for d in dow.index]
        ax.bar(dow.index, dow.values, color=bar_cols, edgecolor="none", width=0.6)
        ax.set_xticklabels([d[:3] for d in dow.index], color=TEXT, fontsize=9)
        rupee_fmt(ax)
        show(fig)


# ══════════════════════════════════════════════════════════════
#  TAB 3 — MY EXPENSES
# ══════════════════════════════════════════════════════════════

with tab3:
    df_show = st.session_state.df.copy()
    if df_show.empty:
        st.info("No expenses yet. Add some in the Add Expense tab.")
    else:
        sc1, sc2, sc3 = st.columns([2,1,1])
        with sc1:
            search = st.text_input("Search", placeholder="description, category, note...")
        with sc2:
            fcat = st.selectbox("Filter Category", ["All"] + sorted(df_show["category"].unique()))
        with sc3:
            fpay = st.selectbox("Filter Payment", ["All"] + PAYMENT_METHODS)

        dfd = enrich(df_show)
        if search:
            mask = (
                dfd["description"].str.contains(search, case=False, na=False) |
                dfd["category"].str.contains(search, case=False, na=False) |
                dfd["note"].astype(str).str.contains(search, case=False, na=False)
            )
            dfd = dfd[mask]
        if fcat != "All":
            dfd = dfd[dfd["category"] == fcat]
        if fpay != "All":
            dfd = dfd[dfd["payment_method"] == fpay]

        dfd_s = dfd.sort_values("date", ascending=False)
        st.markdown(f"**{len(dfd_s)} of {len(df_show)} expenses — Total: Rs.{dfd_s['amount'].sum():,.2f}**")

        disp = dfd_s.copy()
        disp["date"] = pd.to_datetime(disp["date"]).dt.strftime("%d %b %Y")
        st.dataframe(
            disp[["id","date","category","description","amount","payment_method","note"]],
            use_container_width=True, hide_index=True, height=380
        )

        st.markdown("---")
        ec1, ec2 = st.columns(2)

        with ec1:
            st.markdown("##### Delete an Expense")
            del_id = st.selectbox("Select ID to delete",
                                  ["—"] + df_show["id"].tolist(), key="del_id")
            if st.button("Delete Selected") and del_id != "—":
                row = df_show[df_show["id"]==del_id].iloc[0]
                st.session_state.df = df_show[df_show["id"]!=del_id].reset_index(drop=True)
                save_expenses(st.session_state.df)
                st.success(f"Deleted: {row['description']} — Rs.{row['amount']:,.2f}")
                st.rerun()

        with ec2:
            st.markdown("##### Edit an Expense")
            edit_id = st.selectbox("Select ID to edit",
                                   ["—"] + df_show["id"].tolist(), key="edit_id")
            if edit_id != "—":
                erow = df_show[df_show["id"]==edit_id].iloc[0]
                with st.form("edit_form"):
                    ne_date  = st.date_input("Date", value=pd.to_datetime(erow["date"]).date())
                    ne_cat   = st.selectbox("Category", CATEGORIES,
                                             index=CATEGORIES.index(erow["category"])
                                             if erow["category"] in CATEGORIES else 0)
                    ne_desc  = st.text_input("Description", value=erow["description"])
                    ne_amt   = st.number_input("Amount", value=float(erow["amount"]),
                                               step=10.0, format="%.2f")
                    ne_pay   = st.selectbox("Payment Method", PAYMENT_METHODS,
                                             index=PAYMENT_METHODS.index(erow["payment_method"])
                                             if erow["payment_method"] in PAYMENT_METHODS else 0)
                    ne_note  = st.text_area("Note", value=str(erow.get("note","")))
                    if st.form_submit_button("Save Changes"):
                        idx = df_show[df_show["id"]==edit_id].index[0]
                        st.session_state.df.at[idx,"date"]           = pd.Timestamp(ne_date)
                        st.session_state.df.at[idx,"category"]       = ne_cat
                        st.session_state.df.at[idx,"description"]    = ne_desc
                        st.session_state.df.at[idx,"amount"]         = round(ne_amt,2)
                        st.session_state.df.at[idx,"payment_method"] = ne_pay
                        st.session_state.df.at[idx,"note"]           = ne_note
                        save_expenses(st.session_state.df)
                        st.success("Updated!")
                        st.rerun()


# ══════════════════════════════════════════════════════════════
#  TAB 4 — BUDGET
# ══════════════════════════════════════════════════════════════

with tab4:
    if df_f.empty:
        st.info("Add expenses first to see budget analysis.")
    else:
        budgets  = st.session_state.budgets
        months_n = max(df_f["month_num"].nunique(), 1)
        cat_totals = df_f.groupby("category")["amount"].sum()

        rows = []
        for cat in CATEGORIES:
            total  = cat_totals.get(cat, 0)
            avg    = total / months_n
            budget = budgets.get(cat, DEFAULT_BUDGETS.get(cat, 2000))
            rows.append({
                "category":    cat,
                "total":       total,
                "monthly_avg": avg,
                "budget":      budget,
                "variance":    avg - budget,
                "pct_used":    min((avg/budget*100) if budget else 0, 200),
                "status":      "Over Budget" if avg > budget else "Under Budget",
            })
        bdf = pd.DataFrame(rows).sort_values("variance", ascending=False)

        over  = bdf[bdf["status"]=="Over Budget"]
        under = bdf[bdf["status"]=="Under Budget"]
        bc1,bc2,bc3,bc4 = st.columns(4)
        bc1.metric("Over Budget",  f"{len(over)} cats",  delta_color="inverse")
        bc2.metric("Under Budget", f"{len(under)} cats")
        bc3.metric("Total Budget (monthly)", f"Rs.{bdf['budget'].sum():,.0f}")
        bc4.metric("Total Actual (monthly)", f"Rs.{bdf['monthly_avg'].sum():,.0f}")

        st.markdown("---")
        st.markdown("#### Budget Utilization per Category")
        for _, row in bdf.iterrows():
            pct   = row["pct_used"]
            color = "#ef4444" if row["status"]=="Over Budget" else "#22c55e"
            tag   = (f'<span class="tag tag-over">Over</span>'
                     if row["status"]=="Over Budget"
                     else f'<span class="tag tag-under">Under</span>')
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"margin-bottom:.15rem;'>"
                f"<span style='font-size:.82rem;color:{TEXT};min-width:160px;'>{row['category']}</span>"
                f"<span style='font-size:.78rem;color:#64748b;'>"
                f"Rs.{row['monthly_avg']:,.0f} / Rs.{row['budget']:,.0f}/mo &nbsp; {tag}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.progress(min(pct/100, 1.0))

        st.markdown("---")
        st.markdown("#### Budget vs Actual Chart")
        fig = _fig(14,6)
        ax  = _ax(fig)
        x4  = np.arange(len(bdf))
        w   = 0.35
        ax.bar(x4-w/2, bdf["budget"],      w, label="Budget",
               color="#334155", edgecolor="none", alpha=0.9)
        ax.bar(x4+w/2, bdf["monthly_avg"], w, label="Actual",
               color=["#ef4444" if s=="Over Budget" else "#22c55e"
                      for s in bdf["status"]],
               edgecolor="none", alpha=0.9)
        ax.set_xticks(x4)
        ax.set_xticklabels(bdf["category"], rotation=25, ha="right",
                           fontsize=8, color=TEXT)
        rupee_fmt(ax)
        ax.legend(frameon=False, labelcolor=TEXT, fontsize=9)
        show(fig)


# ══════════════════════════════════════════════════════════════
#  TAB 5 — INSIGHTS
# ══════════════════════════════════════════════════════════════

with tab5:
    if df_f.empty:
        st.info("Add expenses to generate insights.")
    else:
        k          = kpis(df_f)
        budgets    = st.session_state.budgets
        months_n   = max(df_f["month_num"].nunique(), 1)
        cat_totals = df_f.groupby("category")["amount"].sum().sort_values(ascending=False)
        mgrp       = df_f.groupby(["month_num","month"])["amount"].sum().reset_index()
        anom       = detect_anomalies(df_f)
        monthly_sp = k["total"] / months_n
        savings_a  = monthly_income - monthly_sp
        savings_r  = (savings_a / monthly_income * 100) if monthly_income else 0

        insights = []

        insights.append(
            f"You have logged **Rs.{k['total']:,.0f}** across "
            f"**{k['count']} transactions** ({k['date_from']} to {k['date_to']})."
        )

        top_cat = cat_totals.index[0]
        top_pct = cat_totals.iloc[0] / k["total"] * 100
        insights.append(
            f"Biggest spending category: **{top_cat}** — "
            f"Rs.{cat_totals.iloc[0]:,.0f} ({top_pct:.1f}% of total)."
        )

        if len(cat_totals) > 1:
            low_cat = cat_totals.index[-1]
            insights.append(
                f"Lowest spend category: **{low_cat}** — Rs.{cat_totals.iloc[-1]:,.0f}."
            )

        if len(mgrp) >= 2:
            peak_r = mgrp.loc[mgrp["amount"].idxmax()]
            low_r  = mgrp.loc[mgrp["amount"].idxmin()]
            insights.append(f"Peak spending month: **{peak_r['month']}** (Rs.{peak_r['amount']:,.0f}).")
            insights.append(f"Lowest spending month: **{low_r['month']}** (Rs.{low_r['amount']:,.0f}).")

        insights.append(
            f"Average transaction: **Rs.{k['avg']:,.0f}**. "
            f"Largest single spend: Rs.{k['max']:,.0f}."
        )

        if monthly_income > 0:
            label = ("Excellent" if savings_r>=30 else "Good" if savings_r>=20
                     else "Fair" if savings_r>=10 else "Poor — consider cutting expenses")
            insights.append(
                f"Estimated savings rate: **{savings_r:.1f}%** ({label}). "
                f"Saving approx Rs.{max(savings_a,0):,.0f}/month."
            )

        over_cats = []
        for cat, total in cat_totals.items():
            avg_m  = total / months_n
            budget = budgets.get(cat, DEFAULT_BUDGETS.get(cat, 0))
            if avg_m > budget:
                over_cats.append(f"{cat} (+Rs.{avg_m-budget:,.0f}/mo)")
        if over_cats:
            insights.append(
                f"**{len(over_cats)} categories** over budget: "
                + ", ".join(over_cats[:3]) + ("..." if len(over_cats)>3 else "")
            )
        else:
            insights.append("All categories are within budget — excellent discipline!")

        df_f2 = df_f.copy()
        df_f2["is_weekend"] = df_f2["day_of_week"].isin(["Saturday","Sunday"])
        we_avg = df_f2[df_f2["is_weekend"]]["amount"].mean()
        wd_avg = df_f2[~df_f2["is_weekend"]]["amount"].mean()
        if pd.notna(we_avg) and pd.notna(wd_avg) and wd_avg > 0:
            pct_diff = (we_avg - wd_avg) / wd_avg * 100
            insights.append(
                f"Weekend avg: **Rs.{we_avg:,.0f}** vs weekday Rs.{wd_avg:,.0f} "
                f"({pct_diff:+.0f}% difference)."
            )

        top_pay     = df_f.groupby("payment_method")["amount"].sum().idxmax()
        top_pay_pct = df_f.groupby("payment_method")["amount"].sum().max() / k["total"] * 100
        insights.append(f"Mostly pay via **{top_pay}** ({top_pay_pct:.0f}% of spend).")

        if len(anom):
            top_a = anom.iloc[0]
            insights.append(
                f"**{len(anom)} unusual transaction(s)** detected. "
                f"Largest: {top_a['description']} — Rs.{top_a['amount']:,.0f} "
                f"(Z={top_a['z']:.1f} sigma above category norm)."
            )

        date_span = max((pd.to_datetime(df_f["date"].max())
                         - pd.to_datetime(df_f["date"].min())).days, 1)
        insights.append(f"Daily average spend: **Rs.{k['total']/date_span:,.0f}/day**.")

        st.markdown("### Auto-Generated Insights")
        for ins in insights:
            st.markdown(
                f"<div class='insight-row'>{ins}</div>",
                unsafe_allow_html=True
            )

        # Anomaly section
        st.markdown("---")
        st.markdown("### Anomaly Detection (Z-Score Method)")
        if len(anom):
            st.warning(f"{len(anom)} transactions flagged as unusually high in their category.")
            a_disp = anom.copy()
            a_disp["date"]   = pd.to_datetime(a_disp["date"]).dt.strftime("%d %b %Y")
            a_disp["amount"] = a_disp["amount"].map(lambda x: f"Rs.{x:,.2f}")
            a_disp["z"]      = a_disp["z"].map(lambda x: f"{x:.2f}s")
            st.dataframe(
                a_disp[["date","category","description","amount","payment_method","z"]]
                .rename(columns={"z":"Z-Score"}),
                use_container_width=True, hide_index=True
            )
            # Scatter
            fig = _fig(12,5)
            ax  = _ax(fig)
            ax.scatter(pd.to_datetime(df_f["date"]), df_f["amount"],
                       alpha=0.3, color="#60a5fa", s=25, label="Normal")
            ax.scatter(pd.to_datetime(anom["date"]), anom["amount"],
                       color="#ef4444", s=90, zorder=5, marker="D", label="Anomaly")
            rupee_fmt(ax)
            ax.legend(frameon=False, labelcolor=TEXT, fontsize=9)
            ax.set_title("Anomaly Detection Scatter", color=TEXT, fontsize=11, pad=10)
            show(fig)
        else:
            st.success("No anomalies detected in your current dataset.")

        # Correlation heatmap
        if df_f["month_num"].nunique() >= 3 and df_f["category"].nunique() >= 2:
            st.markdown("---")
            st.markdown("### Category Spend Correlation")
            pivot = df_f.pivot_table(
                index="month_num", columns="category",
                values="amount", aggfunc="sum", fill_value=0
            )
            if pivot.shape[1] >= 2:
                import seaborn as sns
                corr = pivot.corr()
                fig  = _fig(8,6)
                ax   = fig.add_subplot(111)
                ax.set_facecolor(CARD)
                sns.heatmap(corr, ax=ax, cmap="coolwarm", center=0,
                            linewidths=0.5, linecolor=BG,
                            annot=True, fmt=".1f", annot_kws={"size":7},
                            cbar_kws={"shrink":.8})
                ax.set_title("Category Correlation (Monthly)", color=TEXT,
                             fontsize=11, pad=10)
                ax.tick_params(colors=TEXT, labelsize=7)
                show(fig)


# ══════════════════════════════════════════════════════════════
#  TAB 6 — HOW TO IMPROVE
# ══════════════════════════════════════════════════════════════

# # with tab6:

#     st.markdown("## How to Improve This Project")
#     st.markdown(
#         "<p style='color:#64748b;font-size:.85rem;'>"
#         "A structured roadmap from student project to production-grade "
#         "financial analytics platform.</p>",
#         unsafe_allow_html=True
#     )

#     # ── Level 1 ──────────────────────────────────────────────
#     st.markdown("---")
#     st.markdown("### Level 1 — Easy Wins (1–3 days each)")

#     l1_items = [
#         ("Bank Statement Import",
#          "Parse real bank CSV/PDF exports (HDFC, SBI, ICICI) using pdfplumber or camelot. "
#          "Auto-map merchant names to categories with fuzzy string matching. "
#          "Eliminates manual entry for real users."),
#         ("PDF Report Export",
#          "Use reportlab or fpdf2 to generate a monthly PDF with embedded charts. "
#          "Users can share it with an accountant or keep as a personal record."),
#         ("Monthly Email Summary",
#          "Use smtplib + schedule to auto-send a monthly email with key stats, "
#          "budget warnings, and top expenses. Zero-touch financial awareness."),
#         ("Smart Auto-Categorization",
#          "Use keyword mapping (Zomato→Food, Uber→Transport) or train a small "
#          "Naive Bayes / TF-IDF classifier on transaction descriptions. "
#          "Reduces manual category selection."),
#         ("Recurring Expense Detection",
#          "Identify repeating expenses (rent, subscriptions) and flag if a known "
#          "recurring payment is missing for the current month. Useful for budgeting."),
#         ("Dark/Light Theme Toggle",
#          "Add a proper theme switch persisted via config file. "
#          "Small UX improvement but shows attention to user experience."),
#     ]

#     c1, c2 = st.columns(2)
#     for i, (title, desc) in enumerate(l1_items):
#         with (c1 if i%2==0 else c2):
#             st.markdown(
#                 f"<div class='improve-card'><h4>{title}</h4><p>{desc}</p></div>",
#                 unsafe_allow_html=True
#             )

#     # ── Level 2 ──────────────────────────────────────────────
#     st.markdown("---")
#     st.markdown("### Level 2 — Intermediate Features (1–2 weeks each)")

#     l2_items = [
#         ("ML Expense Forecasting",
#          "Use Facebook Prophet or ARIMA to predict next month's spend per category. "
#          "Show forecast with confidence intervals. Train on 3+ months of data. "
#          "Directly relevant for Data Scientist roles."),
#         ("Real-time Budget Alerts",
#          "Send push notifications via Telegram Bot API or browser alerts when "
#          "spending crosses 80% or 100% of a monthly budget. Needs background scheduler."),
#         ("SQLite / PostgreSQL Database",
#          "Replace CSV with SQLite (beginner) or PostgreSQL (advanced) via SQLAlchemy. "
#          "Shows database skills critical for DA/DE/BA roles. Enables multi-user support."),
#         ("Multi-User Authentication",
#          "Add Streamlit-Authenticator or FastAPI + JWT auth. "
#          "Each user gets their own isolated expense history. "
#          "Transforms it from a personal tool to a shareable product."),
#         ("Multi-Currency Support",
#          "Use forex-python or Open Exchange Rates API to convert foreign expenses "
#          "to home currency. Essential for frequent travellers."),
#         ("Interactive React Frontend",
#          "Replace Streamlit with React + FastAPI backend. "
#          "Add drag-to-reorder, inline editing, real-time charts via Recharts. "
#          "Production-grade web app experience."),
#     ]

#     c3, c4 = st.columns(2)
#     for i, (title, desc) in enumerate(l2_items):
#         with (c3 if i%2==0 else c4):
#             st.markdown(
#                 f"<div class='improve-card'><h4>{title}</h4><p>{desc}</p></div>",
#                 unsafe_allow_html=True
#             )

#     # ── Level 3 ──────────────────────────────────────────────
#     st.markdown("---")
#     st.markdown("### Level 3 — Advanced / Production (1–4 weeks each)")

#     l3_items = [
#         ("Bank API Integration",
#          "Integrate with Plaid (US) or Finvu / Account Aggregator (India) "
#          "to auto-import transactions in real-time. This is what production fintech apps do."),
#         ("LLM-Powered Financial Advisor",
#          "Send spending summaries to Claude / GPT-4 and generate personalized "
#          "conversational advice: 'You spent 40% on food. Here are 3 ways to save Rs.2,000/month.'"),
#         ("Cloud Deployment with CI/CD",
#          "Dockerize the app, deploy on AWS EC2 or Streamlit Cloud, "
#          "add GitHub Actions for auto-deploy on push. Demonstrates DevOps awareness."),
#         ("End-to-End Data Encryption",
#          "Encrypt all financial data at rest (AES-256) and in transit (HTTPS). "
#          "Add 2FA login. Required for any production financial product."),
#         ("Investment Tracking Module",
#          "Track SIP, mutual funds, and stocks alongside expenses. "
#          "Pull live NAV via MF API or Yahoo Finance. "
#          "Show net worth = assets minus liabilities over time."),
#         ("Voice / OCR Expense Entry",
#          "Allow users to photograph a receipt or speak an expense. "
#          "Use Tesseract OCR + Whisper STT to auto-extract amount, merchant, date. "
#          "Removes friction from expense logging entirely."),
#     ]

#     c5, c6 = st.columns(2)
#     for i, (title, desc) in enumerate(l3_items):
#         with (c5 if i%2==0 else c6):
#             st.markdown(
#                 f"<div class='improve-card'><h4>{title}</h4><p>{desc}</p></div>",
#                 unsafe_allow_html=True
#             )

#     # ── Tech stack upgrade table ──────────────────────────────
#     st.markdown("---")
#     st.markdown("### Tech Stack Upgrade Roadmap")
#     st.markdown("""
#     <div style='background:#161628;border:1px solid #252540;border-radius:12px;padding:1.5rem;overflow-x:auto;'>
#     <table style='width:100%;border-collapse:collapse;font-size:.82rem;min-width:600px;'>
#     <thead>
#       <tr style='border-bottom:1px solid #252540;'>
#         <th style='text-align:left;padding:10px 12px;color:#a78bfa;'>Component</th>
#         <th style='text-align:left;padding:10px 12px;color:#a78bfa;'>Current (V1)</th>
#         <th style='text-align:left;padding:10px 12px;color:#a78bfa;'>Intermediate (V2)</th>
#         <th style='text-align:left;padding:10px 12px;color:#a78bfa;'>Production (V3)</th>
#       </tr>
#     </thead>
#     <tbody>
#       <tr style='border-bottom:1px solid #1e1e38;'>
#         <td style='padding:10px 12px;color:#94a3b8;'>Storage</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>CSV File</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>SQLite</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>PostgreSQL / MongoDB</td>
#       </tr>
#       <tr style='border-bottom:1px solid #1e1e38;'>
#         <td style='padding:10px 12px;color:#94a3b8;'>Frontend</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Streamlit</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Dash / Gradio</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>React + FastAPI</td>
#       </tr>
#       <tr style='border-bottom:1px solid #1e1e38;'>
#         <td style='padding:10px 12px;color:#94a3b8;'>Authentication</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>None</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Streamlit-Auth</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>JWT + OAuth2</td>
#       </tr>
#       <tr style='border-bottom:1px solid #1e1e38;'>
#         <td style='padding:10px 12px;color:#94a3b8;'>ML / AI</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Z-Score rules</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Prophet Forecasting</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>LLM Advisor + AutoML</td>
#       </tr>
#       <tr style='border-bottom:1px solid #1e1e38;'>
#         <td style='padding:10px 12px;color:#94a3b8;'>Data Source</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Manual / CSV</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Bank PDF Import</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Plaid / Finvu API</td>
#       </tr>
#       <tr style='border-bottom:1px solid #1e1e38;'>
#         <td style='padding:10px 12px;color:#94a3b8;'>Deployment</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Local only</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Streamlit Cloud</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>AWS / GCP + Docker + K8s</td>
#       </tr>
#       <tr>
#         <td style='padding:10px 12px;color:#94a3b8;'>Alerts</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>None</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Email via SMTP</td>
#         <td style='padding:10px 12px;color:#e2e8f0;'>Telegram Bot + Web Push</td>
#       </tr>
#     </tbody>
#     </table>
#     </div>
#     """, unsafe_allow_html=True)

#     # ── Interview Q&A ─────────────────────────────────────────
#     st.markdown("---")
#     st.markdown("### Interview Q&A — Say This When Asked About Improvements")

#     qa = [
#         ("How would you scale this to 1 million users?",
#          "Migrate to PostgreSQL with proper indexing on user_id, date, and category. "
#          "Add Redis caching for dashboard queries. "
#          "Use Kubernetes with horizontal pod autoscaling. "
#          "Partition data by user_id for fast retrieval. "
#          "Implement CDN for static assets."),
#         ("How would you add ML predictions?",
#          "Train a Facebook Prophet model per category on 6+ months of data. "
#          "Expose predictions via a FastAPI endpoint. "
#          "Re-train weekly using an Airflow DAG. "
#          "Show forecast + confidence intervals in the dashboard chart."),
#         ("How would you handle data privacy?",
#          "AES-256 encryption at rest, HTTPS for all transit, "
#          "no PII in logs, per-user data isolation in DB, "
#          "GDPR-compliant delete API, and regular security audits."),
#         ("What KPIs would you track for this as a product?",
#          "DAU/MAU for engagement, expenses logged per session, "
#          "budget breach rate, D7/D30 retention, "
#          "CSV export count as a trust proxy, and time-to-first-insight after signup."),
#         ("How would you auto-categorize expenses?",
#          "Start with keyword rules (Zomato→Food, Uber→Transport). "
#          "Then train a TF-IDF + Logistic Regression classifier on labeled historical data. "
#          "Improve with a fine-tuned BERT model for production accuracy."),
#     ]

#     for q, a in qa:
#         with st.expander(f"Q: {q}"):
#             st.markdown(
#                 f"<div style='color:#94a3b8;font-size:.85rem;line-height:1.7;"
#                 f"padding:.5rem 0;'>{a}</div>",
#                 unsafe_allow_html=True
#             )

#     st.markdown("---")
#     st.markdown(
#         "<div style='text-align:center;color:#475569;font-size:.78rem;padding:1rem;'>"
#         "Data saved locally to <code>data/user_expenses.csv</code> "
#         "· Built with Python, Pandas, Matplotlib, Streamlit"
#         "</div>",
#         unsafe_allow_html=True
#     )
