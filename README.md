#  Expense Tracker App — using Data Science

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **A complete end-to-end Data Science project** simulating personal expense tracking,
> analysis, visualization, and automated insight generation using Python.
> Built to demonstrate skills relevant to **Data Analyst**, **Business Analyst**,
> and **Financial Analyst** roles.

---

##  Problem Statement

Individuals and businesses often struggle to understand where money goes,
identify overspending, and plan budgets effectively.
This project simulates a full expense tracking pipeline — from raw transaction data
to actionable financial insights — using data science techniques.

---

##  Solution

An end-to-end Python pipeline that:
- Generates **852 realistic synthetic transactions** across 12 expense categories
- Cleans and validates data using Pandas
- Performs **category, monthly, quarterly, payment-method** analysis
- Detects **spending anomalies** using Z-score
- Compares actual spend vs **predefined budgets**
- Generates **12 professional charts** (dark-themed)
- Produces a **full text report** with key insights
- Includes an **interactive Streamlit dashboard**

---

##  Features

| Feature | Description |
|---|---|
|  Synthetic Data Generator | 852 realistic expense records for 2024 |
|  Data Cleaning | Duplicate removal, type validation, null handling |
|  Category Analysis | Breakdown across 12 categories with % share |
|  Monthly Trends | Month-over-month change and visual trend line |
|  Payment Analysis | UPI, Credit Card, Debit Card, Cash, Net Banking |
|  Budget vs Actual | Per-category variance and over/under budget flags |
|  Anomaly Detection | Z-score based unusual transaction flagging |
|  Savings Estimator | Monthly savings rate calculation |
|  Heatmap | Day × Hour spending intensity heatmap |
|  Auto Report | Full text annual report generated automatically |
|  Streamlit Dashboard | Interactive web app with filters |

---

##  Tech Stack

```
Python 3.10+      → Core language
Pandas            → Data manipulation & analysis
NumPy             → Numerical operations
Matplotlib        → Static charts (dark theme)
Seaborn           → Heatmap visualization
Streamlit         → Interactive web dashboard
```

---

##  Project Structure

```
Expense-Tracker-App/
│
├── data/
│   └── expenses.csv           ← Generated synthetic dataset (852 rows)
│
├── src/
│   ├── data_generator.py      ← Synthetic data creation
│   ├── analysis.py            ← All analysis functions
│   ├── visualizations.py      ← 12 chart generators
│   └── insights.py            ← Insight generation + report
│
├── outputs/
│   ├── charts/                ← 12 .png chart files
│   └── annual_report.txt      ← Full text financial report
│
├── notebooks/
│   └── EDA_Notebook.ipynb     ← Jupyter exploration (optional)
│
├── images/                    ← Screenshots for README
│
├── main.py                    ←  Run full pipeline (entry point)
├── app.py                     ←  Streamlit dashboard
├── requirements.txt           ← Python dependencies
└── README.md                  ← This file
```

---

##  How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Expense-Tracker-App.git
cd Expense-Tracker-App
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run full analysis pipeline
```bash
python main.py
```

**Expected outputs:**
- `data/expenses.csv` — 852-row synthetic dataset
- `outputs/charts/*.png` — 12 professional charts
- `outputs/annual_report.txt` — Full financial report

### 5. Launch Streamlit Dashboard (optional)
```bash
streamlit run app.py
```
Open → http://localhost:8501

---

##  Charts Generated

| File | Description |
|---|---|
| `00_dashboard_summary.png` | 4-in-1 overview dashboard |
| `01_category_pie.png` | Spending share by category |
| `02_category_bar.png` | Horizontal bar — category totals |
| `03_monthly_trend.png` | Line chart — monthly spend trend |
| `04_payment_methods.png` | Bar — payment method breakdown |
| `05_weekly_heatmap.png` | Heatmap — day × hour intensity |
| `06_budget_vs_actual.png` | Grouped bar — budget vs actual |
| `07_quarterly_donut.png` | Donut — Q1/Q2/Q3/Q4 distribution |
| `08_top_transactions.png` | Top 10 highest transactions |
| `09_monthly_stacked.png` | Stacked bar — category by month |
| `10_savings_gauge.png` | Polar gauge — savings rate |
| `11_anomalies.png` | Scatter — anomaly detection |

---

##  Key Insights (Sample — 2024)

-  **Total Spent** : ₹15,52,413 across **852 transactions**
-  **Top Category** : Food & Dining (19.8% of total spend)
-  **Peak Month** : May (₹1,86,065)
-  **Top Payment** : UPI (41.7% of all transactions)
-   **11 of 12** categories exceeded monthly budget
- 📆 **Daily Average** : ₹4,253 per day

---

##  Architecture & Workflow

```
 Data Input (Synthetic Generator)
        ↓
 Data Cleaning (Pandas)
        ↓
 Analysis Layer
   ├── Category Analysis
   ├── Monthly Trends
   ├── Payment Breakdown
   ├── Budget Comparison
   ├── Anomaly Detection
   └── Savings Estimation
        ↓
 Visualization Layer (Matplotlib / Seaborn)
        ↓
 Insight Engine (Auto-generated findings)
        ↓
 Output (Charts + Report + Dashboard)
```


##  License

MIT License — free to use, modify, and distribute.

---

##  Author

**Shruti Srivastava**
B.E | Aspiring Data Analyst   
 [LinkedIn] https://www.linkedin.com/in/shruti-srivastava-36b26232a/?skipRedirect=true
