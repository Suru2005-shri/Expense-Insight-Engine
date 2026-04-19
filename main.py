"""
╔══════════════════════════════════════════════════════════╗
║      EXPENSE TRACKER APP — using Data Science            ║
║      Author  : Your Name                                 ║
║      Year    : 2024                                      ║
║      Stack   : Python · Pandas · NumPy · Matplotlib      ║
╚══════════════════════════════════════════════════════════╝

Run:
    python main.py

Outputs:
    data/expenses.csv          ← synthetic dataset
    outputs/annual_report.txt  ← full text report
    outputs/charts/*.png       ← 12 charts
"""

import os
import sys
import time

# ─── Make sure src/ is on the path ───────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_generator import generate_expenses, save_dataset
from analysis import (
    clean_data, summary_stats, category_analysis,
    monthly_trends, payment_analysis, weekday_analysis,
    quarterly_analysis, monthly_category_pivot,
    budget_analysis, top_transactions, detect_anomalies,
    savings_estimate,
)
from visualizations import (
    plot_category_pie, plot_category_bar, plot_monthly_trend,
    plot_payment_methods, plot_weekly_heatmap, plot_budget_vs_actual,
    plot_quarterly, plot_top_transactions, plot_monthly_category_stacked,
    plot_savings_gauge, plot_anomalies, plot_dashboard_summary,
)
from insights import generate_insights, print_report, save_report


def banner(text: str) -> None:
    print(f"\n{'─'*60}")
    print(f"  {text}")
    print(f"{'─'*60}")


def main():
    t0 = time.time()
    os.makedirs("outputs/charts", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # ════════════════════════════════════════════════════════════
    # PHASE 1 — GENERATE SYNTHETIC DATA
    # ════════════════════════════════════════════════════════════
    banner("📦 PHASE 1 — Generating Synthetic Dataset")
    df_raw = generate_expenses(year=2024)
    save_dataset(df_raw, "data/expenses.csv")
    print(f"\n  Preview (first 5 rows):\n{df_raw.head().to_string(index=False)}")

    # ════════════════════════════════════════════════════════════
    # PHASE 2 — CLEAN DATA
    # ════════════════════════════════════════════════════════════
    banner("🧹 PHASE 2 — Data Cleaning")
    df = clean_data(df_raw)

    # ════════════════════════════════════════════════════════════
    # PHASE 3 — ANALYSIS
    # ════════════════════════════════════════════════════════════
    banner("📊 PHASE 3 — Analysis")

    stats      = summary_stats(df)
    cat_df     = category_analysis(df)
    monthly_df = monthly_trends(df)
    pay_df     = payment_analysis(df)
    day_df     = weekday_analysis(df)
    qtr_df     = quarterly_analysis(df)
    pivot      = monthly_category_pivot(df)
    budget_df  = budget_analysis(df)
    top_df     = top_transactions(df, n=10)
    anomalies  = detect_anomalies(df)
    savings    = savings_estimate(df, monthly_income=60000)

    print(f"\n  ✅ Total Spent       : ₹{stats['total_spent']:,.2f}")
    print(f"  ✅ Transactions      : {stats['total_transactions']}")
    print(f"  ✅ Avg Transaction   : ₹{stats['avg_transaction']:,.2f}")
    print(f"  ✅ Anomalies Found   : {len(anomalies)}")
    print(f"  ✅ Savings Rate      : {savings['savings_rate_pct']:.1f}%")

    # ════════════════════════════════════════════════════════════
    # PHASE 4 — VISUALIZATIONS
    # ════════════════════════════════════════════════════════════
    banner("🎨 PHASE 4 — Generating Charts")

    charts = [
        ("Dashboard Summary",         lambda: plot_dashboard_summary(cat_df, monthly_df, pay_df, budget_df)),
        ("Category Pie Chart",        lambda: plot_category_pie(cat_df)),
        ("Category Bar Chart",        lambda: plot_category_bar(cat_df)),
        ("Monthly Trend",             lambda: plot_monthly_trend(monthly_df)),
        ("Payment Methods",           lambda: plot_payment_methods(pay_df)),
        ("Weekly Heatmap",            lambda: plot_weekly_heatmap(df)),
        ("Budget vs Actual",          lambda: plot_budget_vs_actual(budget_df)),
        ("Quarterly Donut",           lambda: plot_quarterly(qtr_df)),
        ("Top Transactions",          lambda: plot_top_transactions(top_df)),
        ("Monthly Stacked Bar",       lambda: plot_monthly_category_stacked(df)),
        ("Savings Gauge",             lambda: plot_savings_gauge(savings)),
        ("Anomaly Detection",         lambda: plot_anomalies(df, anomalies)),
    ]

    for name, fn in charts:
        print(f"\n  ▶ {name}")
        fn()

    # ════════════════════════════════════════════════════════════
    # PHASE 5 — INSIGHTS & REPORT
    # ════════════════════════════════════════════════════════════
    banner("🔍 PHASE 5 — Generating Insights & Report")

    insights = generate_insights(stats, cat_df, monthly_df, budget_df, anomalies, savings)
    print_report(stats, cat_df, monthly_df, pay_df, budget_df,
                 qtr_df, top_df, anomalies, savings, insights)
    save_report(stats, cat_df, monthly_df, pay_df, budget_df,
                qtr_df, top_df, anomalies, savings, insights,
                "outputs/annual_report.txt")

    # ════════════════════════════════════════════════════════════
    # DONE
    # ════════════════════════════════════════════════════════════
    elapsed = time.time() - t0
    print(f"\n{'═'*60}")
    print(f"  🎉  Pipeline complete in {elapsed:.1f}s")
    print(f"  📁  Charts  → outputs/charts/")
    print(f"  📄  Report  → outputs/annual_report.txt")
    print(f"  📊  Dataset → data/expenses.csv")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()
