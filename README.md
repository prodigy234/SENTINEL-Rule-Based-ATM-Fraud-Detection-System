<div align="center">

<img src="https://img.shields.io/badge/🛡️_SENTINEL-Fraud_Intelligence_Platform-0EA5E9?style=for-the-badge&labelColor=040D1A" alt="SENTINEL"/>

# SENTINEL — Bank-Grade ATM & Card Fraud Detection System

**A production-quality, rule-based fraud intelligence platform built with Python and Streamlit**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57.0-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-3.0.2-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-6.7.0-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-22C55E?style=flat-square)]()

---

*Built by **Kajola Gbenga Adewale** · May 2026*

</div>

---

## 📋 Table of Contents

- [What is SENTINEL?](#-what-is-sentinel)
- [The Problem It Solves](#-the-problem-it-solves)
- [Live Demo Screenshots](#-live-demo-screenshots)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Fraud Detection Algorithm](#-fraud-detection-algorithm)
- [Dataset Documentation](#-dataset-documentation-bank_transactionscsv)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Technical Stack](#-technical-stack)
- [Performance Metrics](#-performance-metrics)
- [Background & Context](#-background--context)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🛡️ What is SENTINEL?

**SENTINEL** is a fully interactive, bank-grade ATM and card fraud detection system deployed as a web application. It replicates the core functionality of the fraud monitoring systems used by Nigerian commercial banks — including rule-based transaction screening, real-time risk scoring, customer intelligence profiling, and automated fraud reporting.

The system screens transactions using a **six-rule weighted scoring engine**, assigns every transaction a risk score from 0 to 100, classifies it into a risk tier (CRITICAL / HIGH / MEDIUM / LOW / CLEAR), and surfaces actionable fraud alerts in a professional analyst dashboard.

> **Academic / Training Context:** SENTINEL was developed as the capstone project for Session 3 of the Zedcrest Capital Data Analyst Training Programme (May–August 2026), demonstrating how Python, Pandas, and Streamlit can replicate enterprise fraud detection workflows that typically require expensive commercial software.

---

## 🎯 The Problem It Solves

### The Scale Problem in Nigerian Banking

A mid-sized Nigerian bank processes **50,000+ transactions daily**. A fraud analyst working at full capacity can review approximately 800 transactions per hour. Manual review of the full daily volume would require **62+ simultaneous analysts** — financially impossible for any institution.

| Manual Review | SENTINEL |
|---------------|----------|
| 50,000 transactions reviewed: ~63 hours | 50,000 transactions screened: **< 1 second** |
| Subject to human fatigue and inconsistency | Consistent rules applied identically every time |
| Cannot process overnight transactions in real time | Detects midnight fraud while analyst is off-shift |
| Expensive — requires large analyst headcount | Runs on any laptop or cloud server |
| No quantified accuracy measurement | Precision, Recall, F1 computed automatically |

**SENTINEL automates the first-pass screening** so analysts only receive the transactions that genuinely require human judgment — typically 12–15% of the total, with the highest-risk cases surfaced first.

---

## 📸 Live Demo Screenshots

```
🏠 Command Centre     — Executive fraud dashboard with KPIs, trends, and live alerts
🔍 Live Detection     — Configure rules and run detection with real-time accuracy metrics
📊 Analytics          — Multi-dimensional fraud pattern analysis (temporal, geographic, amounts)
👤 Customer Intel     — Individual account risk profiling and full transaction timeline
📋 Alerts & Reports   — Prioritised fraud alert queue with export functionality
⚙️ Engine Config      — Detection rule documentation and scoring model reference
```

> *Screenshots available after deployment — run `streamlit run sentinel_fraud_app.py` and navigate each page.*

---

## ✨ Features

### 🔍 Fraud Detection Engine
- **6 configurable detection rules** covering the most common Nigerian banking fraud patterns
- **Weighted scoring formula** producing a 0–100 risk score per transaction
- **5 risk tiers**: CRITICAL (85–100), HIGH (70–84), MEDIUM (50–69), LOW (25–49), CLEAR (0–24)
- **3 tunable parameters** (amount multiplier, suspicious hour cutoff, minimum detection score) via interactive sliders
- **Real-time accuracy evaluation**: Precision, Recall, F1 Score, Accuracy, Confusion Matrix

### 📊 Analytics & Intelligence
- Daily, weekly, and hourly fraud trend visualisations
- Geographic fraud distribution (state-level bar chart + treemap)
- Fraud type breakdown (Card Cloning, Skimming, SIM Swap, Account Takeover, etc.)
- Bank-level performance comparison
- Customer profile risk analysis
- Transaction type fraud rate matrix
- Interactive Plotly charts (hover, zoom, pan)

### 👤 Customer Intelligence
- Searchable customer selector (200 customers, sorted by fraud rate)
- Full customer profile card (masked account/card numbers, PCI-DSS compliant)
- Individual transaction timeline with fraud markers
- Hourly activity analysis per customer
- Complete transaction history table

### 📋 Case Management
- Filterable fraud alert queue (by type, bank, amount)
- CRITICAL alerts with full prescribed action blocks
- One-click CSV export (fraud alerts, summary report, full dataset)
- Risk scoring with colour-coded severity badges

### 🎨 Professional UI
- Dark navy design system (#040D1A base)
- Custom fonts: Syne (headings) + DM Mono (data) + Space Grotesk (body)
- Animated system status indicator
- Responsive multi-column layouts
- Mobile-compatible

---

## 🏗️ System Architecture

```
sentinel_fraud_app.py
│
├── CONFIGURATION LAYER
│   ├── st.set_page_config()          — Page title, icon, layout
│   ├── COLORS dict                   — Centralised design tokens
│   ├── apply_theme(fig, **kwargs)    — Plotly dark theme applier
│   └── CSS injection                 — Custom fonts, card styles, animations
│
├── DATA LAYER
│   ├── load_data()                   — CSV reader + type conversion + derived columns
│   │   ├── pd.read_csv()             — Load bank_transactions.csv
│   │   ├── pd.to_datetime()          — Parse datetime strings
│   │   ├── pd.to_numeric()           — Convert amounts to float
│   │   ├── is_fraud_bool column      — Boolean version of is_fraud
│   │   ├── amount_ratio column       — amount / typical_max_amount
│   │   ├── week column               — ISO week number for trend charts
│   │   └── risk_level column         — CRITICAL/HIGH/MEDIUM/LOW/CLEAR label
│   └── @st.cache_data                — Cache result: load once, serve always
│
├── DETECTION ENGINE
│   └── apply_rules(df, multiplier, max_hour, min_risk)
│       ├── Rule 1: amount > typical_max × multiplier      (weight: 30)
│       ├── Rule 2: 0 ≤ hour ≤ max_hour                   (weight: 20)
│       ├── Rule 3: 'FOREIGN' in atm_location             (weight: 30)
│       ├── Rule 4: daily_total > daily_limit              (weight: 25)
│       ├── Rule 5: amount < 500 & physical transaction    (weight: 15)
│       ├── Rule 6: balance_after < 500                   (weight: 10)
│       ├── detection_score = weighted_sum.clip(0, 100)
│       ├── detected_fraud = detection_score >= min_risk
│       └── metrics: TP, FP, FN, TN, Precision, Recall, F1, Accuracy
│
├── NAVIGATION
│   ├── st.session_state.page         — Active page tracker
│   └── st.rerun()                    — Force re-render on page change
│
└── SIX PAGES
    ├── dashboard    — Command Centre (KPIs + charts + alerts feed)
    ├── detection    — Live Detection Engine (sliders + confusion matrix)
    ├── analytics    — Advanced Analytics (4 tabs: temporal/geo/amounts/behaviour)
    ├── customer     — Customer Intelligence (profile + timeline + history)
    ├── alerts       — Alerts & Reports (filtered queue + exports)
    └── config       — Engine Config (rule docs + scoring reference)
```

---

## 🧠 Fraud Detection Algorithm

SENTINEL uses a **Weighted Rule-Based Expert System** — the same approach used as the first detection layer in Nigerian Tier-1 bank fraud operations centres.

### The Six Detection Rules

| # | Rule Name | Condition | Weight | Fraud Pattern Detected |
|---|-----------|-----------|--------|------------------------|
| 1 | **Large Amount** | `amount > typical_max × multiplier` | 30 pts | Card cloning, Account takeover — criminals drain accounts with one large withdrawal |
| 2 | **Unusual Hour** | `0 ≤ hour ≤ max_hour` (midnight–4am) | 20 pts | Night-time fraud — strikes while cardholders sleep and SMS alerts go unread |
| 3 | **Foreign Location** | `'FOREIGN' in atm_location` | 30 pts | Card cloning/skimming — cloned card used in a different state from cardholder's home |
| 4 | **Daily Limit Breach** | `daily_total > daily_limit` | 25 pts | Systematic draining — multiple ATMs used to exceed daily limits |
| 5 | **Micro-Transaction** | `amount < ₦500` on ATM/POS | 15 pts | Card testing — fraudsters verify stolen cards with tiny amounts before large withdrawals |
| 6 | **Near-Zero Balance** | `balance_after < ₦500` | 10 pts | Account draining — account emptied to near-zero; the final stage of a draining attack |

### Scoring Formula

```python
detection_score = (
    rule1_large_amount * 30 +
    rule2_unusual_hour * 20 +
    rule3_foreign_loc  * 30 +
    rule4_limit_breach * 25 +
    rule5_micro_txn    * 15 +
    rule6_near_zero    * 10
).clip(upper=100)
```

> Each rule is a boolean (True=1, False=0). Maximum theoretical score = 130, clipped to 100.

### Risk Classification

```
Score  85–100  →  🔴 CRITICAL  →  Block card · Call customer · File SAR
Score  70–84   →  🟠 HIGH      →  Temporary hold · Analyst review < 30 mins
Score  50–69   →  🟡 MEDIUM    →  Flag for review · Send SMS alert
Score  25–49   →  🔵 LOW       →  Log and monitor
Score   0–24   →  🟢 CLEAR     →  Normal transaction
```

### Why Rule-Based (Not ML)?

| Dimension | Rule-Based (SENTINEL) | Machine Learning |
|-----------|----------------------|------------------|
| Explainability | Full — every flag has a reason | Often opaque |
| Training data needed | Zero | Thousands of labelled examples |
| Regulatory compliance | Preferred by CBN | Requires additional audit tools |
| Deployment time | Hours | Weeks |
| New fraud types | Requires new rule | May auto-detect |
| Performance | Milliseconds for 6,328 rows | Slower for large datasets |

> **Industry Note:** Most Nigerian Tier-1 banks use rule engines as the **primary screening layer** and ML models as a **secondary validation layer** for flagged cases. SENTINEL implements the primary layer.

---

## 📂 Dataset Documentation: `bank_transactions.csv`

### Overview

| Property | Value |
|----------|-------|
| Rows | 6,328 transactions |
| Columns | 29 |
| Customers | 200 unique customers |
| Banks | 10 Nigerian commercial banks |
| Date Range | January 1 – March 31, 2026 (Q1) |
| Fraud Rate | 12.3% (781 fraudulent transactions) |
| Normal Rate | 87.7% (5,547 normal transactions) |

### Fraud Type Distribution

| Fraud Type | Count | % of Fraud | Description |
|------------|-------|------------|-------------|
| Card Cloning | 250 | 32.0% | Magnetic stripe copied; clone used elsewhere |
| Skimming | 163 | 20.9% | Device attached to ATM captures card data |
| Account Takeover | 107 | 13.7% | Credentials stolen; full account control |
| Card Testing | 99 | 12.7% | Micro-transactions to verify stolen card |
| SIM Swap | 66 | 8.5% | Phone number hijacked to bypass 2FA |
| Phishing | 49 | 6.3% | Cardholder tricked into revealing credentials |
| Limit Breach | 47 | 6.0% | Daily spending limit exceeded |

### Customer Profiles

| Profile | Typical Max/Txn | Daily Limit | Avg Transactions/Month |
|---------|----------------|-------------|----------------------|
| `low` | ₦500 – ₦10,000 | ₦50,000 | 5 |
| `medium` | ₦2,000 – ₦50,000 | ₦150,000 | 12 |
| `high` | ₦10,000 – ₦200,000 | ₦500,000 | 20 |
| `premium` | ₦50,000 – ₦1,000,000 | ₦2,000,000 | 30 |

### Complete Column Reference

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `transaction_id` | string | TXN0000001 | Unique transaction identifier (TXN + 7 digits) |
| `datetime` | datetime | 2026-01-15 02:34:18 | Full timestamp (YYYY-MM-DD HH:MM:SS) |
| `date` | date | 2026-01-15 | Calendar date only |
| `time` | string | 02:34:18 | Time in HH:MM:SS format |
| `hour` | integer | 2 | Hour of day (0–23); pre-computed for fast filtering |
| `day_of_week` | string | Saturday | Full day name |
| `month` | string | January | Full month name |
| `customer_id` | string | CUST00096 | Unique customer identifier (CUST + 5 digits) |
| `customer_name` | string | Musa Okafor | Full customer name |
| `account_number` | string | 0123456789 | 10-digit NUBAN account number |
| `card_last4` | string | 4821 | Last 4 digits of payment card |
| `card_type` | string | Visa Debit | Card network and product type |
| `bank` | string | GTBank | Issuing bank name |
| `transaction_type` | string | ATM Withdrawal | Type of transaction |
| `merchant` | string | Shoprite | Merchant name (POS/Online only) |
| `amount_naira` | float | 87432.50 | Transaction value in Nigerian Naira (₦) |
| `balance_before` | float | 350000.00 | Account balance before transaction |
| `balance_after` | float | 262567.50 | Account balance after transaction |
| `atm_location` | string | ATM_LG_002 - Victoria Island | ATM/terminal location; fraud injections contain `[FOREIGN]` marker |
| `home_state` | string | Lagos | Customer's registered home state |
| `customer_profile` | string | medium | Spending tier (low/medium/high/premium) |
| `typical_max_amount` | float | 50000.00 | Customer's normal per-transaction maximum |
| `daily_limit` | float | 150000.00 | Bank-set daily spending cap |
| `daily_total_so_far` | float | 87432.50 | Cumulative daily spend at time of transaction |
| `transaction_status` | string | Successful | Processing outcome (Successful/Declined/Reversed) |
| `risk_score` | integer | 92 | Ground-truth risk score (0–100); used for accuracy evaluation |
| `is_fraud` | string | YES | Ground truth fraud label (YES/NO) |
| `fraud_type` | string | Card Cloning | Specific fraud category (empty for normal transactions) |
| `fraud_reason` | string | Amount 8.7× above max | Plain-English explanation of why the transaction was flagged |

> **Note on Synthetic Data:** `bank_transactions.csv` is a synthetic dataset generated using statistically realistic distributions and documented Nigerian banking fraud patterns. It is designed for training, demonstration, and research purposes. No real customer data is used.

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- A terminal / command prompt

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/sentinel-fraud-detection.git
cd sentinel-fraud-detection
```

### Step 2 — Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

```
streamlit==1.57.0    # Web application framework
pandas==3.0.2        # Data manipulation and analysis
plotly==6.7.0        # Interactive charting library
scikit-learn==1.8.0  # Machine learning utilities
numpy==2.4.4         # Numerical computing
```

### Step 4 — Verify the Dataset is Present

Ensure both files are in the **same directory**:

```
sentinel-fraud-detection/
├── sentinel_fraud_app.py       ✅
├── bank_transactions.csv       ✅
├── requirements.txt            ✅
└── README.md                   ✅
```

### Step 5 — Run the Application

```bash
streamlit run sentinel_fraud_app.py
```

The application will open automatically in your default browser at:

```
Local URL:   http://localhost:8501
Network URL: http://YOUR_IP:8501
```

---

## 📖 Usage Guide

### 🏠 Command Centre (First Page)

The dashboard loads automatically. No action required. It shows:
- **KPI cards** — total transactions, fraud count, fraud value, total volume, recall rate
- **Daily trend chart** — fraud count and fraud rate over Q1 2026
- **Fraud type chart** — breakdown by attack vector
- **Hour-of-day chart** — when fraud peaks (midnight–4am highlighted in red)
- **Bank performance** — fraud rate per institution
- **Critical alerts** — top 5 highest-risk transactions

---

### 🔍 Live Detection Engine

1. **Adjust the three sliders** to configure detection sensitivity:
   - `AMOUNT MULTIPLIER` — raise to reduce false alarms; lower to catch more fraud
   - `SUSPICIOUS HOUR CUTOFF` — transactions up to this hour are flagged
   - `MINIMUM DETECTION SCORE` — the threshold for classifying a transaction as fraud
2. **(Optional)** Expand `ADVANCED FILTERS` to narrow the analysis to specific banks, transaction types, or customer profiles
3. Click **RUN DETECTION ENGINE**
4. Review the output:
   - 6 accuracy metric cards (Precision, Recall, F1, Accuracy, TP, FP)
   - Confusion matrix heatmap
   - Detection score distribution with threshold line
   - Flagged transactions table (sortable)
   - CSV export button

**Tuning Tips:**

| Goal | Action |
|------|--------|
| Fewer false alarms (higher precision) | Raise Amount Multiplier OR raise Min Score |
| Catch more fraud (higher recall) | Lower Amount Multiplier OR lower Min Score |
| Focus on overnight fraud | Lower Suspicious Hour Cutoff to 2 |
| Test one bank only | Use Advanced Filters → select one bank |

---

### 📊 Analytics

Click `Analytics` in the sidebar. Four tabs:

- **TEMPORAL** — weekly trends, day-of-week patterns, fraud heatmap (hour × day)
- **GEOGRAPHIC** — state-level fraud rates, treemap by fraud case count
- **AMOUNTS** — box plots of normal vs fraud amounts, amount band breakdown
- **BEHAVIOUR** — sunburst (transaction type → fraud type), profile scatter plot

---

### 👤 Customer Intelligence

1. Click `Customer Intel` in the sidebar
2. Use the **SELECT CUSTOMER** dropdown (pre-sorted: highest fraud rate first)
3. Type to search by name
4. The page loads:
   - Customer profile card (name, account, card, bank, profile tier)
   - 4 metric cards (transaction count, fraud flags, daily limit, typical max)
   - Transaction timeline scatter (blue dots = normal, red X = fraud)
   - Hourly activity stacked bar chart
   - Full transaction history table

---

### 📋 Alerts & Reports

1. Click `Alerts & Reports` in the sidebar
2. Use the three **filters** to narrow the alert list:
   - Fraud Type (e.g. show only Card Cloning)
   - Bank (e.g. show only GTBank)
   - Minimum Amount (e.g. show only alerts ≥ ₦100,000)
3. **CRITICAL alerts** (risk score ≥ 85) appear as red toast notifications with prescribed actions
4. **All filtered alerts** appear in the sortable table below
5. Use the **Export Centre** to download:
   - Fraud Alerts CSV (for operations team)
   - Summary Report CSV (for management)
   - Full Dataset CSV (for further analysis)

---

### ⚙️ Engine Config

Reference page — no interactive elements. Documents:
- All 6 detection rules with conditions, weights, and fraud patterns
- Risk classification thresholds and prescribed actions
- Dataset column dictionary

---

## 📁 Project Structure

```
sentinel-fraud-detection/
│
├── sentinel_fraud_app.py        # Main application (1,446 lines)
│   ├── Lines 1–32               # Imports and page configuration
│   ├── Lines 33–70              # Design system (colors + apply_theme)
│   ├── Lines 71–473             # CSS injection (fonts, cards, animations)
│   ├── Lines 474–512            # load_data() — CSV loading + preprocessing
│   ├── Lines 513–596            # apply_rules() — fraud detection engine
│   ├── Lines 597–677            # Sidebar navigation + helper functions
│   ├── Lines 678–837            # Page: Command Centre (dashboard)
│   ├── Lines 838–964            # Page: Live Detection Engine
│   ├── Lines 965–1110           # Page: Advanced Analytics (4 tabs)
│   ├── Lines 1111–1250          # Page: Customer Intelligence
│   ├── Lines 1251–1354          # Page: Alerts & Reports
│   └── Lines 1355–1446          # Page: Engine Configuration
│
├── bank_transactions.csv        # Synthetic transaction dataset
│   ├── 6,328 rows               # Transactions
│   ├── 29 columns               # Features per transaction
│   ├── 200 customers            # Unique account holders
│   ├── 10 banks                 # Nigerian commercial banks
│   └── 12.3% fraud rate         # 781 injected fraud cases
│
├── requirements.txt             # Python dependencies (5 packages)
│
└── README.md                    # This file
```

---

## 🛠️ Technical Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Web Framework** | Streamlit | 1.57.0 | Browser-based interactive dashboard |
| **Data Processing** | Pandas | 3.0.2 | DataFrame operations, filtering, aggregation |
| **Visualisation** | Plotly | 6.7.0 | Interactive charts (15+ chart types) |
| **Numerical** | NumPy | 2.4.4 | Array operations, clipping, boolean masks |
| **ML Foundation** | scikit-learn | 1.8.0 | ML utilities; architecture ready for model layer |
| **Language** | Python | 3.13 | Core application language |
| **Fonts** | Google Fonts | — | Syne (display) + DM Mono (code) + Space Grotesk (body) |
| **Data Format** | CSV | — | Dataset storage and export |

---

## 📈 Performance Metrics

Results using default parameters (multiplier=3.0, max_hour=4, min_risk=50) on the full 6,328-row dataset:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Precision** | ~64% | 64 of every 100 alerts are genuine fraud |
| **Recall** | ~82% | 82% of all real fraud cases are caught |
| **F1 Score** | ~72% | Balanced precision-recall performance |
| **Accuracy** | ~87% | Overall correct classification rate |
| **True Positives** | ~641 | Real fraud cases correctly detected |
| **False Positives** | ~360 | Normal transactions incorrectly flagged |
| **False Negatives** | ~140 | Real fraud cases missed |
| **True Negatives** | ~5,187 | Normal transactions correctly cleared |
| **Processing Time** | < 1 second | For full 6,328-row scan |

> **Note:** Exact metrics vary based on slider configuration. Higher Amount Multiplier → higher Precision, lower Recall. Lower Min Risk Score → higher Recall, lower Precision.

### Tuning for Different Risk Appetites

```
Conservative (fewer false alarms):  multiplier=4.0, min_risk=60
Balanced (default):                 multiplier=3.0, min_risk=50
Aggressive (catch more fraud):      multiplier=2.0, min_risk=35
```

---

## 🎓 Background & Context

SENTINEL was developed as the Session 3 project of the **Zedcrest Capital Data Analyst Training Programme** (May–August 2026), a 30-session Python, R, and Machine Learning training programme designed to equip data analysts with production-level analytical skills.

**Programme Objectives:**
1. Prepare the analyst for the IBM Data Science Professional Certificate (target: August 7, 2026)
2. Embed advanced analytics directly into Zedcrest Capital's organisational decision-making

**Session 3 Learning Outcomes** demonstrated by SENTINEL:
- Loading and processing real-world CSV data with Pandas
- Applying comparison operators and boolean logic to financial data
- Using `for` loops to process all transactions automatically
- Defining reusable functions (detection rules, scoring, alert generation)
- Measuring system accuracy with precision, recall, F1 score
- Building a professional interactive web application with Streamlit

**Trainer:** Kajola Gbenga Adewale | Prodigy Training Hub | +234 903 878 0790

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] **Machine Learning Layer** — Isolation Forest for unsupervised anomaly detection as a second screening layer on rule-passed transactions
- [ ] **Real-Time Streaming** — WebSocket connection to replace CSV with live transaction feeds
- [ ] **Automated Alerts** — SMS/email notifications via Termii or Twilio API for CRITICAL detections
- [ ] **Card Blocking API** — Integration with card management system API to auto-block flagged cards

### Version 3.0 (Future)
- [ ] **Role-Based Access Control** — Separate analyst, manager, and auditor views
- [ ] **Case Management Workflow** — Mark alerts as Confirmed Fraud / False Positive / Under Investigation
- [ ] **CBN Regulatory Reports** — Auto-generate fraud reports in CBN-mandated format
- [ ] **Audit Logging** — Full tamper-evident audit trail of every detection decision
- [ ] **Multi-Currency Support** — USD, GBP alongside NGN for dollar-denominated funds

---

## 🤝 Contributing

Contributions are welcome! This project is actively maintained for training and research purposes.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m 'Add: description of change'`
4. **Push** to your branch: `git push origin feature/your-feature-name`
5. **Open** a Pull Request

### Contribution Ideas

- Add a new fraud detection rule (Rule 7+)
- Implement the Isolation Forest ML layer
- Add more Nigerian states and ATM locations to the dataset
- Improve the UI with additional chart types
- Write unit tests for the `apply_rules()` function
- Add support for loading external CSV files via file upload

### Code Style

- Follow PEP 8 Python style guidelines
- Add docstrings to all new functions
- Comment complex logic inline
- Test with the provided dataset before submitting

---

## 📜 License

```
MIT License

Copyright (c) 2026 Kajola Gbenga Adewale / Prodigy Training Hub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👤 Author

<div align="center">

**Kajola Gbenga Adewale**

*Data Science Trainer | Python Developer | Analytics Consultant*

Prodigy Training Hub · Lagos, Nigeria

📧 [Your Email] &nbsp;|&nbsp; 📱 +234 903 878 0790 &nbsp;|&nbsp; 🔗 [LinkedIn] &nbsp;|&nbsp; 🐙 [GitHub]

---

*If SENTINEL was useful to you, please ⭐ star the repository — it helps others discover the project.*

</div>

---

<div align="center">

**SENTINEL** is built with ❤️ for the Nigerian banking and fintech community.

*"The for loop is not just a coding tool — it is the mechanism by which computers process in one second what would take a human analyst a week."*
— Kajola Gbenga, Session 3

</div>
