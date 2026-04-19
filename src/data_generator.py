

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ─── Seed for reproducibility ────────────────────────────────────────────────
np.random.seed(42)

# ─── Configuration ───────────────────────────────────────────────────────────
CATEGORIES = {
    "Food & Dining":    {"min": 100,  "max": 2500,  "freq": 20},
    "Rent":             {"min": 8000, "max": 15000, "freq": 1},
    "Transportation":   {"min": 50,   "max": 800,   "freq": 15},
    "Entertainment":    {"min": 200,  "max": 3000,  "freq": 6},
    "Utilities":        {"min": 500,  "max": 2000,  "freq": 3},
    "Healthcare":       {"min": 200,  "max": 5000,  "freq": 2},
    "Shopping":         {"min": 300,  "max": 8000,  "freq": 5},
    "Education":        {"min": 500,  "max": 10000, "freq": 2},
    "Travel":           {"min": 2000, "max": 25000, "freq": 1},
    "Subscriptions":    {"min": 99,   "max": 999,   "freq": 4},
    "Groceries":        {"min": 500,  "max": 4000,  "freq": 8},
    "Personal Care":    {"min": 100,  "max": 2000,  "freq": 4},
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

PAYMENT_WEIGHTS = {
    "UPI": 0.40,
    "Credit Card": 0.25,
    "Debit Card": 0.20,
    "Cash": 0.10,
    "Net Banking": 0.05,
}

DESCRIPTIONS = {
    "Food & Dining":  ["Zomato Order", "Restaurant Bill", "Swiggy Delivery", "Cafe Visit", "Team Lunch"],
    "Rent":           ["Monthly Rent", "House Rent", "Flat Rent"],
    "Transportation": ["Ola Cab", "Uber Ride", "Metro Card Recharge", "Petrol", "Auto Rickshaw"],
    "Entertainment":  ["Movie Tickets", "Netflix", "Amazon Prime", "Concert Tickets", "Gaming"],
    "Utilities":      ["Electricity Bill", "Water Bill", "Gas Bill", "Internet Bill"],
    "Healthcare":     ["Doctor Consultation", "Pharmacy", "Lab Tests", "Medicine"],
    "Shopping":       ["Myntra Order", "Amazon Shopping", "Flipkart", "Clothes", "Accessories"],
    "Education":      ["Course Fee", "Books", "Online Course", "Workshop", "Certification"],
    "Travel":         ["Flight Ticket", "Hotel Booking", "Bus Ticket", "Train Ticket", "Goa Trip"],
    "Subscriptions":  ["Spotify", "YouTube Premium", "Cloud Storage", "Software License"],
    "Groceries":      ["Big Basket", "DMart Groceries", "Milk & Bread", "Vegetables", "Monthly Kirana"],
    "Personal Care":  ["Salon Visit", "Gym Membership", "Skincare Products", "Haircut"],
}


def generate_expenses(year: int = 2024, n_transactions: int = 400) -> pd.DataFrame:
    """
    Generate a synthetic expense DataFrame for the given year.

    Parameters
    ----------
    year : int
        Calendar year to generate data for.
    n_transactions : int
        Approximate total number of transactions.

    Returns
    -------
    pd.DataFrame
    """
    records = []
    start = datetime(year, 1, 1)
    end   = datetime(year, 12, 31)
    date_range = (end - start).days

    for category, cfg in CATEGORIES.items():
        # number of transactions for this category = freq * 12
        n = cfg["freq"] * 12
        for _ in range(n):
            # random date in the year
            rand_days = np.random.randint(0, date_range)
            txn_date  = start + timedelta(days=int(rand_days))

            amount = round(np.random.uniform(cfg["min"], cfg["max"]), 2)

            payment = np.random.choice(
                list(PAYMENT_WEIGHTS.keys()),
                p=list(PAYMENT_WEIGHTS.values())
            )

            desc = np.random.choice(DESCRIPTIONS[category])

            records.append({
                "date":           txn_date,
                "category":       category,
                "description":    desc,
                "amount":         amount,
                "payment_method": payment,
                "month":          txn_date.strftime("%B"),
                "month_num":      txn_date.month,
                "week":           txn_date.isocalendar()[1],
                "day_of_week":    txn_date.strftime("%A"),
                "quarter":        f"Q{(txn_date.month - 1) // 3 + 1}",
            })

    df = pd.DataFrame(records).sort_values("date").reset_index(drop=True)
    df["transaction_id"] = ["TXN" + str(i).zfill(4) for i in range(1, len(df) + 1)]
    df = df[["transaction_id", "date", "category", "description",
             "amount", "payment_method", "month", "month_num",
             "week", "day_of_week", "quarter"]]
    return df


def save_dataset(df: pd.DataFrame, path: str = "data/expenses.csv") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f" Dataset saved → {path}  ({len(df)} rows)")


if __name__ == "__main__":
    df = generate_expenses()
    save_dataset(df, "data/expenses.csv")
    print(df.head(10).to_string())
