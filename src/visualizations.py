"""
visualizations.py
-----------------
All chart functions for the Expense Tracker project.
Each function saves a .png to outputs/charts/ AND returns the figure.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ─── Style Configuration ─────────────────────────────────────────────────────
OUTPUT_DIR = "outputs/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PALETTE      = "Set2"
BG_COLOR     = "#0f0f1a"
CARD_COLOR   = "#1a1a2e"
TEXT_COLOR   = "#e0e0e0"
ACCENT_COLOR = "#7c3aed"
GRID_COLOR   = "#2a2a3e"

CATEGORY_COLORS = {
    "Food & Dining":  "#f97316",
    "Rent":           "#ef4444",
    "Transportation": "#3b82f6",
    "Entertainment":  "#a855f7",
    "Utilities":      "#06b6d4",
    "Healthcare":     "#22c55e",
    "Shopping":       "#ec4899",
    "Education":      "#eab308",
    "Travel":         "#14b8a6",
    "Subscriptions":  "#8b5cf6",
    "Groceries":      "#84cc16",
    "Personal Care":  "#fb923c",
}

def _style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(CARD_COLOR)
    ax.set_title(title, color=TEXT_COLOR, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, color=TEXT_COLOR, fontsize=10)
    ax.set_ylabel(ylabel, color=TEXT_COLOR, fontsize=10)
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.spines["left"].set_color(GRID_COLOR)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, color=GRID_COLOR, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

def _fig(w=12, h=6):
    fig = plt.figure(figsize=(w, h), facecolor=BG_COLOR)
    return fig

def _save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  Saved → {path}")
    return path


# ─── 1. CATEGORY PIE CHART ───────────────────────────────────────────────────

def plot_category_pie(cat_df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(10, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    categories = cat_df["category"].tolist()
    totals     = cat_df["total"].tolist()
    colors     = [CATEGORY_COLORS.get(c, "#888") for c in categories]

    wedges, texts, autotexts = ax.pie(
        totals,
        labels=None,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(edgecolor=BG_COLOR, linewidth=2),
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(8)

    ax.legend(
        wedges, categories,
        loc="center left", bbox_to_anchor=(1, 0.5),
        fontsize=9, frameon=False,
        labelcolor=TEXT_COLOR
    )
    ax.set_title(" Spending by Category", color=TEXT_COLOR,
                 fontsize=15, fontweight="bold", pad=20)
    return _save(fig, "01_category_pie.png")


# ─── 2. CATEGORY BAR CHART ───────────────────────────────────────────────────

def plot_category_bar(cat_df: pd.DataFrame) -> str:
    fig = _fig(14, 7)
    ax  = fig.add_subplot(111)

    colors = [CATEGORY_COLORS.get(c, "#888") for c in cat_df["category"]]
    bars = ax.barh(cat_df["category"], cat_df["total"],
                   color=colors, edgecolor="none", height=0.6)

    # Value labels
    for bar, val in zip(bars, cat_df["total"]):
        ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", ha="left",
                color=TEXT_COLOR, fontsize=8)

    _style_ax(ax, "Total Spending by Category", "Amount (₹)", "")
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    return _save(fig, "02_category_bar.png")


# ─── 3. MONTHLY TREND LINE ───────────────────────────────────────────────────

def plot_monthly_trend(monthly_df: pd.DataFrame) -> str:
    fig = _fig(14, 6)
    ax  = fig.add_subplot(111)

    months = monthly_df["month"].tolist()
    totals = monthly_df["total"].tolist()
    x      = range(len(months))

    ax.fill_between(x, totals, alpha=0.15, color=ACCENT_COLOR)
    ax.plot(x, totals, color=ACCENT_COLOR, linewidth=2.5, marker="o",
            markersize=7, markerfacecolor="white", markeredgecolor=ACCENT_COLOR)

    # Annotate each month
    for xi, (m, t) in enumerate(zip(months, totals)):
        ax.annotate(f"₹{t/1000:.1f}K",
                    xy=(xi, t), xytext=(0, 10),
                    textcoords="offset points",
                    ha="center", color=TEXT_COLOR, fontsize=8)

    ax.set_xticks(list(x))
    ax.set_xticklabels([m[:3] for m in months], rotation=0)
    _style_ax(ax, "📈 Monthly Spending Trend (2024)", "Month", "Amount (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    return _save(fig, "03_monthly_trend.png")


# ─── 4. PAYMENT METHOD BAR ───────────────────────────────────────────────────

def plot_payment_methods(pay_df: pd.DataFrame) -> str:
    fig = _fig(10, 6)
    ax  = fig.add_subplot(111)

    colors = ["#7c3aed", "#3b82f6", "#22c55e", "#f97316", "#ec4899"]
    bars   = ax.bar(pay_df["payment_method"], pay_df["total"],
                    color=colors[:len(pay_df)], edgecolor="none", width=0.5)

    for bar, pct in zip(bars, pay_df["pct_of_total"]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 800,
                f"{pct:.1f}%", ha="center", color=TEXT_COLOR, fontsize=9)

    _style_ax(ax, "💳 Spending by Payment Method", "Payment Method", "Amount (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    return _save(fig, "04_payment_methods.png")


# ─── 5. WEEKLY HEATMAP ───────────────────────────────────────────────────────

def plot_weekly_heatmap(df: pd.DataFrame) -> str:
    """Average spending per day-of-week and hour (simulated)."""
    days  = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    hours = list(range(8, 23))

    np.random.seed(99)
    data = np.random.randint(200, 3000, size=(len(hours), len(days)))
    # Weekend bump
    data[:, 5] = (data[:, 5] * 1.4).astype(int)
    data[:, 6] = (data[:, 6] * 1.3).astype(int)
    # Evening bump
    data[9:14, :] = (data[9:14, :] * 1.5).astype(int)

    fig = _fig(14, 7)
    ax  = fig.add_subplot(111)
    ax.set_facecolor(CARD_COLOR)

    sns.heatmap(
        data, ax=ax,
        xticklabels=[d[:3] for d in days],
        yticklabels=[f"{h}:00" for h in hours],
        cmap="YlOrRd",
        linewidths=0.3,
        linecolor=BG_COLOR,
        annot=False,
        cbar_kws={"label": "Avg ₹ Spent"},
    )
    ax.set_title("Spending Heatmap — Day × Hour", color=TEXT_COLOR,
                 fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    return _save(fig, "05_weekly_heatmap.png")


# ─── 6. BUDGET vs ACTUAL ────────────────────────────────────────────────────

def plot_budget_vs_actual(budget_df: pd.DataFrame) -> str:
    fig = _fig(14, 7)
    ax  = fig.add_subplot(111)

    cats   = budget_df["category"].tolist()
    actual = budget_df["actual_monthly_avg"].tolist()
    budget = budget_df["budget"].tolist()
    x      = np.arange(len(cats))
    w      = 0.35

    b1 = ax.bar(x - w/2, budget, w, label="Budget",
                color="#3b82f6", edgecolor="none", alpha=0.85)
    b2 = ax.bar(x + w/2, actual, w, label="Actual",
                color=[("#ef4444" if a > b else "#22c55e")
                       for a, b in zip(actual, budget)],
                edgecolor="none", alpha=0.85)

    _style_ax(ax, "Budget vs Actual Monthly Spend", "", "Amount (₹)")
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace(" & ", "\n& ").replace(" ", "\n", 1)
                        for c in cats], rotation=0, fontsize=7.5, color=TEXT_COLOR)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    ax.legend(frameon=False, labelcolor=TEXT_COLOR, fontsize=9)
    return _save(fig, "06_budget_vs_actual.png")


# ─── 7. QUARTERLY DONUT ──────────────────────────────────────────────────────

def plot_quarterly(qtr_df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 7), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    colors = ["#7c3aed", "#3b82f6", "#22c55e", "#f97316"]
    wedges, texts, autotexts = ax.pie(
        qtr_df["total"],
        labels=qtr_df["quarter"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        pctdistance=0.80,
        wedgeprops=dict(width=0.5, edgecolor=BG_COLOR, linewidth=3),
    )
    for t in texts:
        t.set_color(TEXT_COLOR)
        t.set_fontsize(12)
        t.set_fontweight("bold")
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(10)

    ax.set_title("Quarterly Spending Distribution",
                 color=TEXT_COLOR, fontsize=14, fontweight="bold", pad=20)
    return _save(fig, "07_quarterly_donut.png")


# ─── 8. TOP TRANSACTIONS ────────────────────────────────────────────────────

def plot_top_transactions(top_df: pd.DataFrame) -> str:
    fig = _fig(14, 6)
    ax  = fig.add_subplot(111)

    labels = [f"{row['description']}\n({row['category']})"
              for _, row in top_df.iterrows()]
    colors = [CATEGORY_COLORS.get(c, "#888") for c in top_df["category"]]

    bars = ax.barh(labels, top_df["amount"], color=colors, edgecolor="none", height=0.6)
    for bar, val in zip(bars, top_df["amount"]):
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", color=TEXT_COLOR, fontsize=8)

    _style_ax(ax, "Top 10 Highest Transactions", "Amount (₹)", "")
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    return _save(fig, "08_top_transactions.png")


# ─── 9. MONTHLY CATEGORY STACKED BAR ────────────────────────────────────────

def plot_monthly_category_stacked(df: pd.DataFrame) -> str:
    pivot = df.pivot_table(
        index="month_num", columns="category",
        values="amount", aggfunc="sum", fill_value=0
    )
    pivot.index = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"][:len(pivot)]

    fig = _fig(16, 7)
    ax  = fig.add_subplot(111)
    ax.set_facecolor(CARD_COLOR)

    colors = [CATEGORY_COLORS.get(c, "#888") for c in pivot.columns]
    pivot.plot(kind="bar", stacked=True, ax=ax, color=colors,
               edgecolor="none", width=0.6)

    _style_ax(ax, "📆 Monthly Spending Breakdown by Category", "Month", "Amount (₹)")
    ax.xaxis.set_tick_params(rotation=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=7,
              frameon=False, labelcolor=TEXT_COLOR)
    return _save(fig, "09_monthly_stacked.png")


# ─── 10. SAVINGS GAUGE ───────────────────────────────────────────────────────

def plot_savings_gauge(savings: dict) -> str:
    rate   = min(max(savings["savings_rate_pct"], 0), 100)
    income = savings["monthly_income"]
    spend  = savings["monthly_spend"]
    saved  = savings["monthly_savings"]

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=BG_COLOR,
                           subplot_kw=dict(polar=True))
    ax.set_facecolor(BG_COLOR)

    # Gauge arc
    theta = np.linspace(0, np.pi, 200)
    ax.plot(theta, [1]*200, color=GRID_COLOR, linewidth=18, solid_capstyle="round")

    # Fill arc proportional to savings rate
    fill_theta = np.linspace(0, np.pi * rate / 100, 200)
    color = "#22c55e" if rate >= 20 else ("#f97316" if rate >= 10 else "#ef4444")
    ax.plot(fill_theta, [1]*200, color=color, linewidth=18, solid_capstyle="round")

    ax.set_ylim(0, 1.5)
    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)
    ax.axis("off")

    ax.text(np.pi/2, 0.3, f"{rate:.1f}%", ha="center", va="center",
            fontsize=28, color=color, fontweight="bold",
            transform=ax.transData)
    ax.text(np.pi/2, 0.0, "Savings Rate", ha="center", va="center",
            fontsize=10, color=TEXT_COLOR, transform=ax.transData)

    fig.text(0.5, 0.05,
             f"Income: ₹{income:,.0f}  |  Spent: ₹{spend:,.0f}  |  Saved: ₹{saved:,.0f}",
             ha="center", color=TEXT_COLOR, fontsize=10)
    fig.suptitle(" Monthly Savings Overview",
                 color=TEXT_COLOR, fontsize=14, fontweight="bold", y=0.95)
    return _save(fig, "10_savings_gauge.png")


# ─── 11. ANOMALY SCATTER ─────────────────────────────────────────────────────

def plot_anomalies(df: pd.DataFrame, anomalies: pd.DataFrame) -> str:
    fig = _fig(14, 6)
    ax  = fig.add_subplot(111)

    ax.scatter(df["date"], df["amount"],
               alpha=0.35, color="#60a5fa", s=20, label="Normal")
    ax.scatter(anomalies["date"], anomalies["amount"],
               color="#ef4444", s=80, zorder=5, label="Anomaly", marker="D")

    for _, row in anomalies.head(5).iterrows():
        ax.annotate(row["description"],
                    xy=(row["date"], row["amount"]),
                    xytext=(10, 10), textcoords="offset points",
                    color="#fbbf24", fontsize=7,
                    arrowprops=dict(arrowstyle="->", color="#fbbf24", lw=0.8))

    _style_ax(ax, "⚠️  Anomaly Detection — Unusual Transactions",
              "Date", "Amount (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    ax.legend(frameon=False, labelcolor=TEXT_COLOR, fontsize=9)
    return _save(fig, "11_anomalies.png")


# ─── 12. DASHBOARD SUMMARY (4-in-1) ─────────────────────────────────────────

def plot_dashboard_summary(cat_df, monthly_df, pay_df, budget_df) -> str:
    fig = plt.figure(figsize=(18, 10), facecolor=BG_COLOR)
    fig.suptitle("Expense Tracker ",
                 color=TEXT_COLOR, fontsize=18, fontweight="bold", y=0.98)

    # ── Plot 1: Category Pie ──────────────────────────────────────────────
    ax1 = fig.add_subplot(2, 3, 1)
    ax1.set_facecolor(CARD_COLOR)
    colors = [CATEGORY_COLORS.get(c, "#888") for c in cat_df["category"]]
    ax1.pie(cat_df["total"], labels=None, colors=colors,
            startangle=140, wedgeprops=dict(edgecolor=BG_COLOR, linewidth=1.5))
    ax1.set_title("Spend by Category", color=TEXT_COLOR, fontsize=11, fontweight="bold")
    ax1.legend(cat_df["category"], loc="lower center",
               fontsize=5.5, frameon=False, labelcolor=TEXT_COLOR,
               bbox_to_anchor=(0.5, -0.25), ncol=2)

    # ── Plot 2: Monthly Trend ─────────────────────────────────────────────
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.set_facecolor(CARD_COLOR)
    x = range(len(monthly_df))
    ax2.fill_between(x, monthly_df["total"], alpha=0.2, color=ACCENT_COLOR)
    ax2.plot(x, monthly_df["total"], color=ACCENT_COLOR, linewidth=2,
             marker="o", markersize=5, markerfacecolor="white")
    ax2.set_xticks(list(x))
    ax2.set_xticklabels([m[:3] for m in monthly_df["month"]], fontsize=7, color=TEXT_COLOR)
    ax2.tick_params(colors=TEXT_COLOR)
    ax2.set_title("Monthly Trend", color=TEXT_COLOR, fontsize=11, fontweight="bold")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    for spine in ["top", "right"]:
        ax2.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax2.spines[spine].set_color(GRID_COLOR)
    ax2.yaxis.grid(True, color=GRID_COLOR, linestyle="--", alpha=0.4)

    # ── Plot 3: Payment Methods ───────────────────────────────────────────
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.set_facecolor(CARD_COLOR)
    pcols = ["#7c3aed","#3b82f6","#22c55e","#f97316","#ec4899"]
    ax3.bar(pay_df["payment_method"], pay_df["total"],
            color=pcols[:len(pay_df)], edgecolor="none", width=0.5)
    ax3.set_title("Payment Methods", color=TEXT_COLOR, fontsize=11, fontweight="bold")
    ax3.tick_params(colors=TEXT_COLOR, labelsize=7)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    for spine in ["top", "right"]:
        ax3.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax3.spines[spine].set_color(GRID_COLOR)
    ax3.yaxis.grid(True, color=GRID_COLOR, linestyle="--", alpha=0.4)

    # ── Plot 4: Budget vs Actual ──────────────────────────────────────────
    ax4 = fig.add_subplot(2, 1, 2)
    ax4.set_facecolor(CARD_COLOR)
    cats   = budget_df["category"].tolist()
    actual = budget_df["actual_monthly_avg"].tolist()
    budget = budget_df["budget"].tolist()
    x4     = np.arange(len(cats))
    w      = 0.35
    ax4.bar(x4 - w/2, budget, w, label="Budget", color="#3b82f6", edgecolor="none", alpha=0.8)
    ax4.bar(x4 + w/2, actual, w, label="Actual",
            color=[("#ef4444" if a > b else "#22c55e") for a, b in zip(actual, budget)],
            edgecolor="none", alpha=0.8)
    ax4.set_xticks(x4)
    ax4.set_xticklabels(cats, rotation=20, ha="right", fontsize=8, color=TEXT_COLOR)
    ax4.set_title("Budget vs Actual", color=TEXT_COLOR, fontsize=11, fontweight="bold")
    ax4.tick_params(colors=TEXT_COLOR)
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v/1000:.0f}K"))
    ax4.legend(frameon=False, labelcolor=TEXT_COLOR, fontsize=8)
    for spine in ["top", "right"]:
        ax4.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax4.spines[spine].set_color(GRID_COLOR)
    ax4.yaxis.grid(True, color=GRID_COLOR, linestyle="--", alpha=0.4)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return _save(fig, "00_dashboard_summary.png")
