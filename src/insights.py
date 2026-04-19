"""
insights.py
-----------
Generates human-readable financial insights and a text report
from the analysed expense data.
"""

import pandas as pd
import os


def generate_insights(
    stats:      dict,
    cat_df:     pd.DataFrame,
    monthly_df: pd.DataFrame,
    budget_df:  pd.DataFrame,
    anomalies:  pd.DataFrame,
    savings:    dict,
) -> list[str]:
    """
    Returns a list of insight strings derived from analysis results.
    """
    insights = []

    # ── Total spend ──────────────────────────────────────────────────────────
    insights.append(
        f"Total spent in 2024 : ₹{stats['total_spent']:,.2f} "
        f"across {stats['total_transactions']} transactions."
    )

    # ── Top category ─────────────────────────────────────────────────────────
    top_cat = cat_df.iloc[0]
    insights.append(
        f" Highest spending category : {top_cat['category']} "
        f"(₹{top_cat['total']:,.2f}, {top_cat['pct_of_total']:.1f}% of total)."
    )

    # ── Lowest category ───────────────────────────────────────────────────────
    low_cat = cat_df.iloc[-1]
    insights.append(
        f" Lowest spending category : {low_cat['category']} "
        f"(₹{low_cat['total']:,.2f})."
    )

    # ── Peak spending month ───────────────────────────────────────────────────
    peak = monthly_df.loc[monthly_df["total"].idxmax()]
    insights.append(
        f" Peak spending month : {peak['month']} (₹{peak['total']:,.2f})."
    )

    # ── Lowest spending month ─────────────────────────────────────────────────
    low_month = monthly_df.loc[monthly_df["total"].idxmin()]
    insights.append(
        f" Lowest spending month : {low_month['month']} (₹{low_month['total']:,.2f})."
    )

    # ── Average transaction ───────────────────────────────────────────────────
    insights.append(
        f"Average transaction amount : ₹{stats['avg_transaction']:,.2f}."
    )

    # ── Over-budget categories ────────────────────────────────────────────────
    over = budget_df[budget_df["status"].str.contains("Over")]
    if len(over):
        cats = ", ".join(over["category"].tolist())
        insights.append(f"  Over-budget categories ({len(over)}) : {cats}.")
    else:
        insights.append(" All categories are within budget — great discipline!")

    # ── Under-budget categories ───────────────────────────────────────────────
    under = budget_df[budget_df["status"].str.contains("Under")]
    insights.append(
        f" Under-budget categories : {len(under)} out of {len(budget_df)}."
    )

    # ── Savings ──────────────────────────────────────────────────────────────
    rate = savings["savings_rate_pct"]
    label = (
        " Excellent" if rate >= 30
        else " Good"   if rate >= 20
        else " Fair"   if rate >= 10
        else " Poor"
    )
    insights.append(
        f"Savings rate : {rate:.1f}%  ({label}) — "
        f"saving ₹{savings['monthly_savings']:,.2f}/month."
    )

    # ── Anomalies ────────────────────────────────────────────────────────────
    if len(anomalies):
        top_anomaly = anomalies.iloc[0]
        insights.append(
            f"Largest anomaly : {top_anomaly['description']} — "
            f"₹{top_anomaly['amount']:,.2f} (Z={top_anomaly['z_score']:.1f}). "
            f"Total unusual transactions : {len(anomalies)}."
        )

    # ── Avg daily spend ───────────────────────────────────────────────────────
    daily_avg = stats["total_spent"] / 365
    insights.append(f"Average daily spend : ₹{daily_avg:,.2f}.")

    return insights


def print_report(
    stats:      dict,
    cat_df:     pd.DataFrame,
    monthly_df: pd.DataFrame,
    pay_df:     pd.DataFrame,
    budget_df:  pd.DataFrame,
    qtr_df:     pd.DataFrame,
    top_df:     pd.DataFrame,
    anomalies:  pd.DataFrame,
    savings:    dict,
    insights:   list,
) -> None:
    """Print a formatted console report."""
    sep  = "─" * 65
    sep2 = "═" * 65

    print(f"\n{sep2}")
    print("EXPENSE TRACKER ")
    print(f"{sep2}")

    # Summary Stats
    print(f"\n{'SUMMARY':^65}")
    print(sep)
    print(f"  Date Range        : {stats['date_range']}")
    print(f"  Total Spent       : ₹{stats['total_spent']:>12,.2f}")
    print(f"  Total Transactions: {stats['total_transactions']:>6}")
    print(f"  Avg Transaction   : ₹{stats['avg_transaction']:>12,.2f}")
    print(f"  Max Transaction   : ₹{stats['max_transaction']:>12,.2f}")
    print(f"  Categories        : {stats['unique_categories']}")

    # Category Table
    print(f"\n{'SPENDING BY CATEGORY':^65}")
    print(sep)
    print(f"  {'#':<3} {'Category':<22} {'Total':>12} {'Count':>6} {'Share':>7}")
    print(f"  {'─'*3} {'─'*22} {'─'*12} {'─'*6} {'─'*7}")
    for _, row in cat_df.iterrows():
        print(f"  {int(row['rank']):<3} {row['category']:<22} "
              f"₹{row['total']:>10,.0f} {int(row['count']):>6} "
              f"{row['pct_of_total']:>6.1f}%")

    # Monthly Trends
    print(f"\n{'MONTHLY TRENDS':^65}")
    print(sep)
    print(f"  {'Month':<12} {'Total':>12} {'Count':>6} {'MoM Δ':>12}")
    print(f"  {'─'*12} {'─'*12} {'─'*6} {'─'*12}")
    for _, row in monthly_df.iterrows():
        mom = f"₹{row['mom_change']:>+,.0f}" if pd.notna(row["mom_change"]) else "   —"
        print(f"  {row['month']:<12} ₹{row['total']:>10,.0f} "
              f"{int(row['count']):>6} {mom:>12}")

    # Payment Methods
    print(f"\n{'PAYMENT METHODS':^65}")
    print(sep)
    for _, row in pay_df.iterrows():
        bar = "" * int(row["pct_of_total"] / 2)
        print(f"  {row['payment_method']:<14} {bar:<22} "
              f"₹{row['total']:>10,.0f}  ({row['pct_of_total']:.1f}%)")

    # Budget Analysis
    print(f"\n{'BUDGET vs ACTUAL':^65}")
    print(sep)
    print(f"  {'Category':<22} {'Budget':>10} {'Actual':>10} {'Status'}")
    print(f"  {'─'*22} {'─'*10} {'─'*10} {'─'*20}")
    for _, row in budget_df.iterrows():
        print(f"  {row['category']:<22} ₹{row['budget']:>8,.0f} "
              f"₹{row['actual_monthly_avg']:>8,.0f}  {row['status']}")

    # Top 5 Transactions
    print(f"\n{'TOP 5 TRANSACTIONS':^65}")
    print(sep)
    for i, (_, row) in enumerate(top_df.head(5).iterrows(), 1):
        print(f"  {i}. {row['description']:<30} ₹{row['amount']:>10,.2f}  "
              f"({row['category']})")

    # Anomalies
    print(f"\n{'ANOMALIES DETECTED':^65}")
    print(sep)
    if len(anomalies):
        for _, row in anomalies.head(5).iterrows():
            print(f"  {row['description']:<28} ₹{row['amount']:>10,.2f}  "
                  f"Z={row['z_score']:.2f}")
    else:
        print("  No anomalies detected.")

    # Savings
    print(f"\n{'SAVINGS OVERVIEW':^65}")
    print(sep)
    print(f"  Monthly Income  : ₹{savings['monthly_income']:>10,.2f}")
    print(f"  Monthly Spend   : ₹{savings['monthly_spend']:>10,.2f}")
    print(f"  Monthly Savings : ₹{savings['monthly_savings']:>10,.2f}")
    print(f"  Savings Rate    : {savings['savings_rate_pct']:>9.1f}%")

    # Insights
    print(f"\n{'KEY INSIGHTS':^65}")
    print(sep)
    for ins in insights:
        print(f"  {ins}")

    print(f"\n{sep2}\n")


def save_report(
    stats, cat_df, monthly_df, pay_df, budget_df, qtr_df,
    top_df, anomalies, savings, insights,
    path: str = "outputs/annual_report.txt"
) -> None:
    """Save the text report to a file."""
    import io, sys
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    print_report(stats, cat_df, monthly_df, pay_df, budget_df,
                 qtr_df, top_df, anomalies, savings, insights)

    sys.stdout = old_stdout
    with open(path, "w", encoding="utf-8") as f:
        f.write(buffer.getvalue())
    print(f"  Report saved → {path}")
