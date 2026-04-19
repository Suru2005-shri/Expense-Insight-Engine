"""
analysis.py
-----------
Data cleaning, EDA, feature engineering, and business insights
for the Expense Tracker project.
"""

import pandas as pd
import numpy as np


# ─── 1. DATA CLEANING ────────────────────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the expense DataFrame.
    - Parse dates
    - Drop duplicates
    - Remove negative / zero amounts
    - Fill missing descriptions
    """
    df = df.copy()

    # Parse date column
    df["date"] = pd.to_datetime(df["date"])

    # Remove duplicates (handle both 'id' and 'transaction_id' column names)
    before = len(df)
    id_col = "transaction_id" if "transaction_id" in df.columns else "id"
    if id_col in df.columns:
        df = df.drop_duplicates(subset=[id_col])
    else:
        df = df.drop_duplicates()
    print(f"  Duplicates removed : {before - len(df)}")

    # Remove bad amounts
    bad = df["amount"] <= 0
    df = df[~bad]
    print(f"  Zero/negative rows removed : {bad.sum()}")

    # Fill missing descriptions
    df["description"] = df["description"].fillna("Unknown")

    # Ensure dtypes
    df["amount"] = df["amount"].astype(float)
    if "month_num" in df.columns:
        df["month_num"] = df["month_num"].astype(int)

    print(f"  Clean dataset shape : {df.shape}")
    return df.reset_index(drop=True)


# ─── 2. SUMMARY STATISTICS ───────────────────────────────────────────────────

def summary_stats(df: pd.DataFrame) -> dict:
    """Return high-level summary figures."""
    stats = {
        "total_spent":        round(df["amount"].sum(), 2),
        "avg_transaction":    round(df["amount"].mean(), 2),
        "max_transaction":    round(df["amount"].max(), 2),
        "min_transaction":    round(df["amount"].min(), 2),
        "total_transactions": len(df),
        "date_range":         f"{df['date'].min().date()} → {df['date'].max().date()}",
        "unique_categories":  df["category"].nunique(),
        "months_covered":     df["month_num"].nunique() if "month_num" in df.columns else df["date"].dt.month.nunique(),
    }
    return stats


# ─── 3. CATEGORY ANALYSIS ────────────────────────────────────────────────────

def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spending by category."""
    cat = (
        df.groupby("category")["amount"]
        .agg(total="sum", count="count", avg="mean", max="max")
        .reset_index()
    )
    cat["pct_of_total"] = (cat["total"] / cat["total"].sum() * 100).round(2)
    cat = cat.sort_values("total", ascending=False).reset_index(drop=True)
    cat["rank"] = cat.index + 1
    return cat


# ─── 4. MONTHLY TRENDS ───────────────────────────────────────────────────────

def monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly spending aggregated across all categories."""
    df = df.copy()
    if "month_num" not in df.columns:
        df["month_num"] = pd.to_datetime(df["date"]).dt.month
    if "month" not in df.columns:
        df["month"] = pd.to_datetime(df["date"]).dt.strftime("%B")
    monthly = (
        df.groupby(["month_num", "month"])["amount"]
        .agg(total="sum", count="count", avg="mean")
        .reset_index()
        .sort_values("month_num")
        .reset_index(drop=True)
    )
    # Month-over-month change
    monthly["mom_change"]    = monthly["total"].diff().round(2)
    monthly["mom_change_pct"]= (monthly["total"].pct_change() * 100).round(2)
    return monthly


# ─── 5. PAYMENT METHOD ANALYSIS ──────────────────────────────────────────────

def payment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Breakdown by payment method."""
    pay = (
        df.groupby("payment_method")["amount"]
        .agg(total="sum", count="count", avg="mean")
        .reset_index()
        .sort_values("total", ascending=False)
        .reset_index(drop=True)
    )
    pay["pct_of_total"] = (pay["total"] / pay["total"].sum() * 100).round(2)
    return pay


# ─── 6. WEEKDAY ANALYSIS ─────────────────────────────────────────────────────

def weekday_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Average spending by day of week."""
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day = (
        df.groupby("day_of_week")["amount"]
        .agg(total="sum", count="count", avg="mean")
        .reindex(order)
        .reset_index()
    )
    return day


# ─── 7. QUARTERLY ANALYSIS ───────────────────────────────────────────────────

def quarterly_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Spending per quarter."""
    qtr = (
        df.groupby("quarter")["amount"]
        .agg(total="sum", count="count", avg="mean")
        .reset_index()
        .sort_values("quarter")
    )
    qtr["pct_of_total"] = (qtr["total"] / qtr["total"].sum() * 100).round(2)
    return qtr


# ─── 8. MONTHLY CATEGORY HEATMAP DATA ────────────────────────────────────────

def monthly_category_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot: rows=category, columns=month_num, values=sum(amount)."""
    pivot = df.pivot_table(
        index="category",
        columns="month_num",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )
    return pivot


# ─── 9. BUDGET ANALYSIS ──────────────────────────────────────────────────────

MONTHLY_BUDGET = {
    "Food & Dining":    5000,
    "Rent":             12000,
    "Transportation":   3000,
    "Entertainment":    4000,
    "Utilities":        3000,
    "Healthcare":       3000,
    "Shopping":         5000,
    "Education":        8000,
    "Travel":           10000,
    "Subscriptions":    1500,
    "Groceries":        6000,
    "Personal Care":    2000,
}

def budget_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare actual monthly average spend vs budget per category.
    Flags over-budget categories.
    """
    actual = df.groupby("category")["amount"].sum() / 12  # monthly avg
    budget = pd.Series(MONTHLY_BUDGET, name="budget")

    result = pd.DataFrame({
        "actual_monthly_avg": actual.round(2),
        "budget":             budget,
    }).dropna()

    result["variance"]      = (result["actual_monthly_avg"] - result["budget"]).round(2)
    result["status"]        = result["variance"].apply(
        lambda x: "Over Budget" if x > 0 else "Under Budget"
    )
    result["over_budget_pct"] = (result["variance"] / result["budget"] * 100).round(2)
    return result.reset_index().rename(columns={"index": "category"})


# ─── 10. TOP TRANSACTIONS ────────────────────────────────────────────────────

def top_transactions(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N most expensive transactions."""
    return df.nlargest(n, "amount")[
        ["transaction_id", "date", "category", "description", "amount", "payment_method"]
    ].reset_index(drop=True)


# ─── 11. ANOMALY DETECTION ───────────────────────────────────────────────────

def detect_anomalies(df: pd.DataFrame, z_thresh: float = 2.5) -> pd.DataFrame:
    """
    Flag transactions whose amount is more than z_thresh standard deviations
    above the category mean (Z-score method).
    """
    df = df.copy()
    df["z_score"] = df.groupby("category")["amount"].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    anomalies = df[df["z_score"] > z_thresh].copy()
    anomalies = anomalies.sort_values("z_score", ascending=False)
    return anomalies[["transaction_id", "date", "category", "description",
                       "amount", "payment_method", "z_score"]].reset_index(drop=True)


# ─── 12. SAVINGS ESTIMATE ────────────────────────────────────────────────────

def savings_estimate(df: pd.DataFrame, monthly_income: float = 60000) -> dict:
    """Estimate monthly savings vs a given income."""
    monthly_spend = df["amount"].sum() / 12
    savings       = monthly_income - monthly_spend
    savings_rate  = (savings / monthly_income) * 100
    return {
        "monthly_income":  monthly_income,
        "monthly_spend":   round(monthly_spend, 2),
        "monthly_savings": round(savings, 2),
        "savings_rate_pct": round(savings_rate, 2),
    }
