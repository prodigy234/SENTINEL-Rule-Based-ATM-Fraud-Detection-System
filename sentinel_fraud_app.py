"""
╔══════════════════════════════════════════════════════════════════════╗
║   SENTINEL - Bank-Grade ATM & Card Fraud Detection System            ║                                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SENTINEL | Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ──────────────────────────────────────────────────────────────
COLORS = {
    "bg_deep":     "#040D1A",
    "bg_card":     "#071528",
    "bg_panel":    "#0A1F38",
    "border":      "#0E3A6E",
    "border_glow": "#1A6DB5",
    "accent_blue": "#0EA5E9",
    "accent_cyan": "#22D3EE",
    "accent_gold": "#F59E0B",
    "red_high":    "#EF4444",
    "red_mid":     "#F97316",
    "yellow":      "#EAB308",
    "green":       "#22C55E",
    "text_primary":"#F0F9FF",
    "text_dim":    "#94A3B8",
    "text_muted":  "#475569",
    "chart_seq":   ["#0EA5E9","#22D3EE","#38BDF8","#7DD3FC","#BAE6FD"],
}

def apply_theme(fig, **kwargs):
    """Apply the SENTINEL dark theme to any plotly figure, then apply extra kwargs."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'DM Mono', monospace", color=COLORS["text_dim"], size=12),
        xaxis=dict(gridcolor="#0E3A6E", linecolor="#0E3A6E", tickcolor=COLORS["text_muted"]),
        yaxis=dict(gridcolor="#0E3A6E", linecolor="#0E3A6E", tickcolor=COLORS["text_muted"]),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#0E3A6E"),
    )
    if kwargs:
        fig.update_layout(**kwargs)
    return fig

# Keep for backward compat
PLOT_TEMPLATE = dict(layout=dict(paper_bgcolor="rgba(0,0,0,0)"))

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600&display=swap');

:root {
    --bg-deep:     #040D1A;
    --bg-card:     #071528;
    --bg-panel:    #0A1F38;
    --border:      #0E3A6E;
    --border-glow: #1A6DB5;
    --accent:      #0EA5E9;
    --cyan:        #22D3EE;
    --gold:        #F59E0B;
    --red:         #EF4444;
    --orange:      #F97316;
    --yellow:      #EAB308;
    --green:       #22C55E;
    --text:        #F0F9FF;
    --dim:         #94A3B8;
    --muted:       #475569;
}

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg-deep);
    color: var(--text);
}
.stApp { background: var(--bg-deep); }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061020 0%, #040D1A 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container { padding-top: 0; }
[data-testid="stSidebarContent"] { padding: 0; }

/* ── HIDE DEFAULT ELEMENTS ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── METRIC CARDS ── */
.sentinel-metric {
    background: linear-gradient(135deg, #071528 0%, #0A1F38 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.sentinel-metric::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent-color, var(--accent));
}
.sentinel-metric:hover { border-color: var(--border-glow); }
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--dim);
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    line-height: 1;
    color: var(--text);
    margin-bottom: 4px;
}
.metric-sub {
    font-size: 12px;
    color: var(--dim);
    font-family: 'DM Mono', monospace;
}
.metric-badge {
    position: absolute;
    top: 16px; right: 16px;
    font-size: 22px;
    opacity: 0.7;
}

/* ── ALERT CARDS ── */
.alert-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 4px solid var(--alert-color, var(--accent));
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: all 0.2s;
}
.alert-card:hover {
    border-color: var(--alert-color, var(--accent));
    box-shadow: 0 0 20px rgba(14, 165, 233, 0.08);
}
.alert-txn-id {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--dim);
    letter-spacing: 1px;
}
.alert-amount {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
}
.alert-customer { font-size: 13px; color: var(--dim); }
.alert-rules { font-size: 11px; color: var(--muted); margin-top: 6px; font-family: 'DM Mono', monospace; }

/* ── RISK BADGE ── */
.risk-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    font-family: 'DM Mono', monospace;
}
.risk-critical { background: rgba(239,68,68,0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
.risk-high     { background: rgba(249,115,22,0.15); color: #F97316; border: 1px solid rgba(249,115,22,0.3); }
.risk-medium   { background: rgba(234,179,8,0.15);  color: #EAB308; border: 1px solid rgba(234,179,8,0.3); }
.risk-low      { background: rgba(34,197,94,0.15);  color: #22C55E; border: 1px solid rgba(34,197,94,0.3); }

/* ── SECTION HEADERS ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
}

/* ── SYSTEM BANNER ── */
.system-banner {
    background: linear-gradient(90deg, #040D1A 0%, #071A35 50%, #040D1A 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.system-banner::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at 50% 50%, rgba(14,165,233,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.banner-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.5px;
}
.banner-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--dim);
    letter-spacing: 2px;
    margin-top: 4px;
}
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--green);
    margin-right: 8px;
    box-shadow: 0 0 6px rgba(34,197,94,0.8);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── TABLE STYLING ── */
.stDataFrame { border: 1px solid var(--border); border-radius: 8px; }
.stDataFrame table { background: var(--bg-card); }
.stDataFrame th {
    background: var(--bg-panel) !important;
    color: var(--accent) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}
.stDataFrame td {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

/* ── INPUTS & FILTERS ── */
.stSelectbox > div > div,
.stSlider > div,
.stMultiSelect > div > div,
.stDateInput > div > div {
    background: var(--bg-panel) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
label[data-testid="stWidgetLabel"] {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--dim) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #0EA5E9, #0284C7);
    border: none;
    color: white;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 10px 24px;
    border-radius: 8px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #38BDF8, #0EA5E9);
    box-shadow: 0 0 20px rgba(14,165,233,0.3);
    transform: translateY(-1px);
}
.stDownloadButton > button {
    background: transparent;
    border: 1px solid var(--border-glow);
    color: var(--accent);
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    border-radius: 8px;
    padding: 8px 20px;
}
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    color: var(--dim);
    padding: 12px 24px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: rgba(14,165,233,0.05);
}

/* ── PROGRESS BARS ── */
.risk-bar-container { margin: 4px 0; }
.risk-bar-bg {
    background: rgba(14,165,233,0.1);
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    color: var(--accent);
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 6px;
}
.streamlit-expanderContent {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 6px 6px;
}

/* ── SIDEBAR ITEMS ── */
.sidebar-logo {
    padding: 24px 20px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}
.sidebar-logo-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.5px;
}
.sidebar-logo-sub {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--dim);
    letter-spacing: 2px;
    margin-top: 2px;
}
.nav-item {
    padding: 10px 20px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    color: var(--dim);
    cursor: pointer;
    border-left: 3px solid transparent;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-item.active {
    color: var(--accent);
    border-left-color: var(--accent);
    background: rgba(14,165,233,0.06);
}
.stat-mini {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 4px 0;
}
.stat-mini-label { font-size: 10px; font-family: 'DM Mono', monospace; color: var(--muted); letter-spacing: 1px; }
.stat-mini-value { font-size: 16px; font-family: 'Syne', sans-serif; font-weight: 700; color: var(--text); margin-top: 2px; }

/* ── CARD GRID ── */
.card-panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    height: 100%;
}
.card-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--dim);
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-glow); }

/* ── TOAST NOTIFICATION ── */
.alert-toast {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from { transform: translateX(10px); opacity: 0; }
    to   { transform: translateX(0);   opacity: 1; }
}

/* ── INFO BOX ── */
.info-box {
    background: rgba(14,165,233,0.06);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 13px;
    color: var(--dim);
    font-family: 'Space Grotesk', sans-serif;
}

/* ── STREAMLIT OVERRIDE ── */
.block-container { padding: 24px 32px; max-width: 1400px; }
[data-testid="stVerticalBlock"] { gap: 16px; }
hr { border-color: var(--border); }
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("bank_transactions.csv")
    except FileNotFoundError:
        st.error("❌ bank_transactions.csv not found. Place it in the same directory.")
        st.stop()
    
    # Parse datetime
    df["datetime"]   = pd.to_datetime(df["datetime"])
    df["date"]       = pd.to_datetime(df["date"])
    df["hour"]       = df["hour"].astype(int)
    df["amount_naira"]       = pd.to_numeric(df["amount_naira"],       errors="coerce")
    df["balance_before"]     = pd.to_numeric(df["balance_before"],     errors="coerce")
    df["balance_after"]      = pd.to_numeric(df["balance_after"],      errors="coerce")
    df["typical_max_amount"] = pd.to_numeric(df["typical_max_amount"], errors="coerce")
    df["daily_limit"]        = pd.to_numeric(df["daily_limit"],        errors="coerce")
    df["daily_total_so_far"] = pd.to_numeric(df["daily_total_so_far"], errors="coerce")
    df["risk_score"]         = pd.to_numeric(df["risk_score"],         errors="coerce")
    
    # Derived columns
    df["is_fraud_bool"] = df["is_fraud"] == "YES"
    df["amount_ratio"]  = df["amount_naira"] / df["typical_max_amount"].clip(lower=1)
    df["week"]          = df["date"].dt.isocalendar().week
    
    # Risk level from risk_score
    def risk_level(score):
        if score >= 85: return "CRITICAL"
        elif score >= 70: return "HIGH"
        elif score >= 50: return "MEDIUM"
        elif score >= 25: return "LOW"
        else: return "CLEAR"
    df["risk_level"] = df["risk_score"].apply(risk_level)
    
    return df

df_full = load_data()

# ── FRAUD DETECTION ENGINE ─────────────────────────────────────────────────────
def apply_rules(df, multiplier=3.0, max_hour=4, min_risk=50):
    """Apply all fraud detection rules and return enriched dataframe."""
    d = df.copy()
    
    # Rule 1: Large amount
    d["rule1_large_amount"] = d["amount_naira"] > (d["typical_max_amount"] * multiplier)
    d["rule1_ratio"]        = (d["amount_naira"] / d["typical_max_amount"].clip(lower=1)).round(1)
    
    # Rule 2: Unusual hour
    d["rule2_unusual_hour"] = (d["hour"] >= 0) & (d["hour"] <= max_hour)
    
    # Rule 3: Foreign location
    d["rule3_foreign_loc"]  = d["atm_location"].str.contains("FOREIGN", na=False)
    
    # Rule 4: Daily limit breach
    d["rule4_limit_breach"] = d["daily_total_so_far"] > d["daily_limit"]
    
    # Rule 5: Micro-transaction (card testing)
    d["rule5_micro_txn"]    = (d["amount_naira"] < 500) & (d["transaction_type"].isin(["ATM Withdrawal","POS Purchase"]))
    
    # Rule 6: Balance near zero after transaction
    d["rule6_near_zero"]    = d["balance_after"] < 500
    
    # Count rules triggered
    rule_cols = ["rule1_large_amount","rule2_unusual_hour","rule3_foreign_loc",
                 "rule4_limit_breach","rule5_micro_txn","rule6_near_zero"]
    d["rules_hit_count"] = d[rule_cols].sum(axis=1)
    
    # Compute detection score (0-100)
    d["detection_score"] = (
        d["rule1_large_amount"].astype(int) * 30 +
        d["rule2_unusual_hour"].astype(int) * 20 +
        d["rule3_foreign_loc"].astype(int)  * 30 +
        d["rule4_limit_breach"].astype(int) * 25 +
        d["rule5_micro_txn"].astype(int)    * 15 +
        d["rule6_near_zero"].astype(int)    * 10
    ).clip(upper=100)
    
    # Detection decision
    d["detected_fraud"] = d["detection_score"] >= min_risk
    
    # Detection label
    def det_label(score):
        if score >= 80: return "🔴 CRITICAL"
        elif score >= 60: return "🟠 HIGH"
        elif score >= 40: return "🟡 MEDIUM"
        elif score >= 20: return "🔵 LOW"
        else: return "🟢 CLEAR"
    d["detection_label"] = d["detection_score"].apply(det_label)
    
    # Build rules explanation
    def build_rules_text(row):
        rules = []
        if row["rule1_large_amount"]: rules.append(f"⚡ Amount {row['rule1_ratio']:.1f}× max")
        if row["rule2_unusual_hour"]: rules.append(f"🌙 Unusual hour ({int(row['hour']):02d}:00)")
        if row["rule3_foreign_loc"]:  rules.append("📍 Foreign location")
        if row["rule4_limit_breach"]: rules.append("🚫 Daily limit breach")
        if row["rule5_micro_txn"]:    rules.append("🔬 Micro-transaction")
        if row["rule6_near_zero"]:    rules.append("⬇ Near-zero balance")
        return " | ".join(rules) if rules else "—"
    d["rules_text"] = d.apply(build_rules_text, axis=1)
    
    # Accuracy metrics
    tp = ((d["detected_fraud"]) & (d["is_fraud_bool"])).sum()
    fp = ((d["detected_fraud"]) & (~d["is_fraud_bool"])).sum()
    fn = ((~d["detected_fraud"]) & (d["is_fraud_bool"])).sum()
    tn = ((~d["detected_fraud"]) & (~d["is_fraud_bool"])).sum()
    precision = tp/(tp+fp)*100 if (tp+fp)>0 else 0
    recall    = tp/(tp+fn)*100 if (tp+fn)>0 else 0
    f1        = 2*precision*recall/(precision+recall) if (precision+recall)>0 else 0
    accuracy  = (tp+tn)/len(d)*100
    
    metrics = dict(tp=int(tp),fp=int(fp),fn=int(fn),tn=int(tn),
                   precision=round(precision,1),recall=round(recall,1),
                   f1=round(f1,1),accuracy=round(accuracy,1))
    return d, metrics

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:28px;">🛡️</span>
            <div>
                <div class="sidebar-logo-title">SENTINEL</div>
                <div class="sidebar-logo-sub">FRAUD INTELLIGENCE PLATFORM</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:8px 20px 4px;font-family:\'DM Mono\',monospace;font-size:10px;letter-spacing:2px;color:#475569;">NAVIGATION</div>', unsafe_allow_html=True)

    pages = {
        "🏠  Command Centre":   "dashboard",
        "🔍  Live Detection":   "detection",
        "📊  Analytics":        "analytics",
        "👤  Customer Intel":   "customer",
        "📋  Alerts & Reports": "alerts",
        "⚙️  Engine Config":    "config",
    }
    
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    
    for label, key in pages.items():
        is_active = st.session_state.page == key
        style = "active" if is_active else ""
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")
    st.markdown('<div style="padding:4px 20px 8px;font-family:\'DM Mono\',monospace;font-size:10px;letter-spacing:2px;color:#475569;">SYSTEM STATUS</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="stat-mini">
            <div class="stat-mini-label">RECORDS</div>
            <div class="stat-mini-value">{len(df_full):,}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        fraud_count = df_full["is_fraud_bool"].sum()
        st.markdown(f"""<div class="stat-mini">
            <div class="stat-mini-label">FRAUD</div>
            <div class="stat-mini-value" style="color:#EF4444;">{fraud_count:,}</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="padding:12px 20px;font-family:'DM Mono',monospace;font-size:11px;color:#22C55E;">
        <span class="status-dot"></span>ENGINE ACTIVE
    </div>
    <div style="padding:0 20px 12px;font-family:'DM Mono',monospace;font-size:10px;color:#475569;">
        v3.1.0 · 6 DETECTION RULES<br>
        Jan 1 – Mar 31, 2026
    </div>
    """, unsafe_allow_html=True)

# ── HELPER FUNCTIONS ───────────────────────────────────────────────────────────
def metric_card(label, value, sub="", color="var(--accent)", icon="", bg_col=None):
    col_style = f"--accent-color:{color};"
    return f"""
    <div class="sentinel-metric" style="{col_style}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {"<div class='metric-sub'>"+sub+"</div>" if sub else ""}
        {"<div class='metric-badge'>"+icon+"</div>" if icon else ""}
    </div>
    """

def styled_chart(fig):
    apply_theme(fig)
    fig.update_traces(marker_line_width=0)
    return fig

def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

def card_start(title=""):
    st.markdown(f'<div class="card-panel"><div class="card-panel-title">{title}</div>', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: COMMAND CENTRE (DASHBOARD)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "dashboard":
    
    # System Banner
    total_fraud = df_full["is_fraud_bool"].sum()
    fraud_rate  = total_fraud/len(df_full)*100
    total_val   = df_full["amount_naira"].sum()
    fraud_val   = df_full[df_full["is_fraud_bool"]]["amount_naira"].sum()
    
    st.markdown(f"""
    <div class="system-banner">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
            <div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span class="status-dot"></span>
                    <span style="font-family:'DM Mono',monospace;font-size:11px;letter-spacing:2px;color:#22C55E;">SYSTEM OPERATIONAL</span>
                </div>
                <div class="banner-title">🛡️ SENTINEL — Fraud Intelligence Command Centre</div>
                <div class="banner-subtitle">REAL-TIME ATM & CARD FRAUD DETECTION · ZEDCREST CAPITAL · Q1 2026</div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'DM Mono',monospace;font-size:11px;color:#475569;">LAST SCAN</div>
                <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#F0F9FF;">Mar 31, 2026 · 23:59</div>
                <div style="font-family:'DM Mono',monospace;font-size:11px;color:#22C55E;margin-top:4px;">✓ ALL SYSTEMS NOMINAL</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row 1
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(metric_card("TOTAL TRANSACTIONS", f"{len(df_full):,}", "Q1 2026", "#0EA5E9", "📊"), unsafe_allow_html=True)
    with c2: st.markdown(metric_card("FRAUD DETECTED", f"{total_fraud:,}", f"{fraud_rate:.1f}% of total", "#EF4444", "🚨"), unsafe_allow_html=True)
    with c3: st.markdown(metric_card("FRAUD VALUE", f"₦{fraud_val/1e6:.1f}M", "Financial exposure", "#F97316", "💰"), unsafe_allow_html=True)
    with c4: st.markdown(metric_card("TOTAL VOLUME", f"₦{total_val/1e9:.2f}B", "All transactions", "#22D3EE", "📈"), unsafe_allow_html=True)
    with c5:
        # Apply rules with defaults for dashboard
        df_det, mets = apply_rules(df_full)
        st.markdown(metric_card("RECALL RATE", f"{mets['recall']}%", f"Precision {mets['precision']}%", "#22C55E", "🎯"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Charts
    c_left, c_right = st.columns([3, 2])
    
    with c_left:
        section_header("📈  DAILY FRAUD TREND — Q1 2026")
        daily = df_full.groupby("date").agg(
            total=("transaction_id","count"),
            fraud=("is_fraud_bool","sum"),
            volume=("amount_naira","sum")
        ).reset_index()
        daily["fraud_rate"] = daily["fraud"] / daily["total"] * 100
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=daily["date"], y=daily["total"], name="Total Txns",
                             marker_color="rgba(14,165,233,0.3)", hovertemplate="Date: %{x}<br>Total: %{y:,}<extra></extra>"), secondary_y=False)
        fig.add_trace(go.Bar(x=daily["date"], y=daily["fraud"], name="Fraud",
                             marker_color="rgba(239,68,68,0.7)", hovertemplate="Fraud: %{y:,}<extra></extra>"), secondary_y=False)
        fig.add_trace(go.Scatter(x=daily["date"], y=daily["fraud_rate"], name="Fraud Rate %",
                                 line=dict(color=COLORS["accent_gold"], width=2), mode="lines",
                                 hovertemplate="Rate: %{y:.1f}%<extra></extra>"), secondary_y=True)
        apply_theme(fig, barmode="overlay", height=280)
        fig.update_layout(legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#0E3A6E",
                                      orientation="h", y=-0.15, x=0))
        fig.update_yaxes(title_text="Transactions", secondary_y=False)
        fig.update_yaxes(title_text="Fraud Rate %", secondary_y=True, gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c_right:
        section_header("🔬  FRAUD TYPE BREAKDOWN")
        fraud_types = df_full[df_full["is_fraud_bool"]]["fraud_type"].value_counts().reset_index()
        fraud_types.columns = ["Type","Count"]
        
        fig2 = px.pie(fraud_types, values="Count", names="Type",
                      color_discrete_sequence=["#0EA5E9","#22D3EE","#F59E0B","#EF4444","#22C55E","#8B5CF6"])
        apply_theme(fig2, height=280, showlegend=True)
        fig2.update_layout(legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#0E3A6E", orientation="v", x=1.0, y=0.5))
        fig2.update_traces(textposition="inside", textinfo="percent",
                           hole=0.45, marker_line_width=2, marker_line_color="#040D1A")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 3: Hour heatmap + Bank breakdown
    c_left2, c_right2 = st.columns([2, 3])

    with c_left2:
        section_header("🌙  FRAUD BY HOUR")
        hour_data = df_full.groupby("hour").agg(
            total=("transaction_id","count"),
            fraud=("is_fraud_bool","sum")
        ).reset_index()
        hour_data["fraud_rate"] = hour_data["fraud"] / hour_data["total"] * 100
        
        fig3 = go.Figure()
        colors_bar = ["#EF4444" if h <= 4 else "#0EA5E9" for h in hour_data["hour"]]
        fig3.add_trace(go.Bar(
            x=hour_data["hour"], y=hour_data["fraud_rate"],
            marker_color=colors_bar,
            hovertemplate="Hour %{x}:00 — Fraud rate: %{y:.1f}%<extra></extra>"
        ))
        apply_theme(fig3, height=260,
                           xaxis_title="Hour of Day", yaxis_title="Fraud %",
                           xaxis=dict(tickmode="linear", tick0=0, dtick=4))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with c_right2:
        section_header("🏦  PERFORMANCE BY BANK")
        bank_data = df_full.groupby("bank").agg(
            total=("transaction_id","count"),
            fraud=("is_fraud_bool","sum"),
            volume=("amount_naira","sum")
        ).reset_index()
        bank_data["fraud_rate"] = (bank_data["fraud"] / bank_data["total"] * 100).round(1)
        bank_data = bank_data.sort_values("fraud_rate", ascending=True)
        
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            y=bank_data["bank"], x=bank_data["fraud_rate"],
            orientation="h",
            marker_color=[COLORS["red_high"] if r > 14 else COLORS["accent_blue"] for r in bank_data["fraud_rate"]],
            text=[f"{r}%" for r in bank_data["fraud_rate"]],
            textposition="outside", textfont_color=COLORS["text_dim"],
            hovertemplate="%{y}: %{x:.1f}% fraud rate<extra></extra>"
        ))
        apply_theme(fig4, height=260,
                           xaxis_title="Fraud Rate (%)", yaxis_title="")
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent critical alerts
    section_header("🚨  CRITICAL ALERTS — LAST 24 HOURS (SIMULATION)")
    critical = df_full[df_full["is_fraud_bool"]].sort_values("risk_score", ascending=False).head(5)
    
    for _, row in critical.iterrows():
        score = row["risk_score"]
        risk_color = "#EF4444" if score >= 85 else "#F97316"
        st.markdown(f"""
        <div class="alert-card" style="--alert-color:{risk_color};">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="alert-txn-id">TXN ID: {row['transaction_id']} &nbsp;·&nbsp; {row['date']} {row['time']}</div>
                    <div class="alert-amount">₦{row['amount_naira']:,.2f}
                        &nbsp;<span style="font-size:13px;color:{risk_color};">{row['fraud_type'].upper()}</span>
                    </div>
                    <div class="alert-customer">👤 {row['customer_name']} &nbsp;·&nbsp; {row['bank']} &nbsp;·&nbsp; {row['card_type']}</div>
                    <div class="alert-rules">⚡ {row['fraud_reason']}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:{risk_color};">{score}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:10px;color:#475569;">RISK SCORE</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LIVE DETECTION
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "detection":
    
    st.markdown("""
    <div class="system-banner">
        <div class="banner-title">🔍 Live Fraud Detection Engine</div>
        <div class="banner-subtitle">APPLY DETECTION RULES TO THE FULL TRANSACTION DATASET IN REAL TIME</div>
    </div>
    """, unsafe_allow_html=True)

    # Filter controls
    c1, c2, c3 = st.columns(3)
    with c1:
        multiplier = st.slider("AMOUNT MULTIPLIER THRESHOLD", 1.5, 6.0, 3.0, 0.5,
                               help="Flag if amount exceeds N× customer's typical max")
    with c2:
        max_hour = st.slider("SUSPICIOUS HOUR CUTOFF (0–N am)", 1, 6, 4, 1,
                             help="Flag transactions between midnight and this hour")
    with c3:
        min_score = st.slider("MINIMUM DETECTION SCORE", 20, 80, 50, 5,
                              help="Minimum score to classify as detected fraud")

    # Additional filters
    with st.expander("🔧  ADVANCED FILTERS"):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            sel_banks = st.multiselect("BANKS", options=sorted(df_full["bank"].unique()),
                                       default=[], placeholder="All banks")
        with fc2:
            sel_types = st.multiselect("TRANSACTION TYPES", options=sorted(df_full["transaction_type"].unique()),
                                       default=[], placeholder="All types")
        with fc3:
            sel_profiles = st.multiselect("CUSTOMER PROFILES", options=sorted(df_full["customer_profile"].unique()),
                                          default=[], placeholder="All profiles")

    # Apply filters
    df_filtered = df_full.copy()
    if sel_banks:    df_filtered = df_filtered[df_filtered["bank"].isin(sel_banks)]
    if sel_types:    df_filtered = df_filtered[df_filtered["transaction_type"].isin(sel_types)]
    if sel_profiles: df_filtered = df_filtered[df_filtered["customer_profile"].isin(sel_profiles)]

    if st.button("🚀  RUN DETECTION ENGINE", use_container_width=True):
        st.session_state.detection_done = True
        st.session_state.det_params = (multiplier, max_hour, min_score)
        st.session_state.df_filtered = df_filtered

    if st.session_state.get("detection_done"):
        m, mh, ms = st.session_state.det_params
        df_work = st.session_state.df_filtered
        df_result, metrics = apply_rules(df_work, m, mh, ms)
        st.session_state.df_result = df_result

        detected = df_result[df_result["detected_fraud"]]
        
        st.markdown("<br>", unsafe_allow_html=True)
        section_header("📊  DETECTION RESULTS")
        
        # Metrics
        mc1,mc2,mc3,mc4,mc5,mc6 = st.columns(6)
        with mc1: st.markdown(metric_card("SCANNED", f"{len(df_work):,}", "transactions", "#0EA5E9"), unsafe_allow_html=True)
        with mc2: st.markdown(metric_card("DETECTED", f"{len(detected):,}", "flagged", "#EF4444"), unsafe_allow_html=True)
        with mc3: st.markdown(metric_card("PRECISION", f"{metrics['precision']}%", "signal quality", "#22C55E"), unsafe_allow_html=True)
        with mc4: st.markdown(metric_card("RECALL", f"{metrics['recall']}%", "fraud coverage", "#F59E0B"), unsafe_allow_html=True)
        with mc5: st.markdown(metric_card("F1 SCORE", f"{metrics['f1']}%", "harmonic mean", "#22D3EE"), unsafe_allow_html=True)
        with mc6: st.markdown(metric_card("ACCURACY", f"{metrics['accuracy']}%", "overall", "#8B5CF6"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Confusion matrix + Score distribution
        cc1, cc2 = st.columns(2)
        with cc1:
            section_header("🔢  CONFUSION MATRIX")
            cm_data = [[metrics["tn"], metrics["fp"]], [metrics["fn"], metrics["tp"]]]
            fig_cm = go.Figure(go.Heatmap(
                z=cm_data, x=["Predicted: NORMAL","Predicted: FRAUD"],
                y=["Actual: NORMAL","Actual: FRAUD"],
                colorscale=[[0,"#071528"],[0.5,"#0EA5E9"],[1,"#22D3EE"]],
                text=[[f"TN: {metrics['tn']:,}", f"FP: {metrics['fp']:,}"],
                      [f"FN: {metrics['fn']:,}", f"TP: {metrics['tp']:,}"]],
                texttemplate="%{text}", textfont_size=16,
                showscale=False,
            ))
            apply_theme(fig_cm, height=280)
            st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

        with cc2:
            section_header("📊  DETECTION SCORE DISTRIBUTION")
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Histogram(
                x=df_result[~df_result["is_fraud_bool"]]["detection_score"],
                name="Normal", marker_color="rgba(14,165,233,0.5)", nbinsx=20,
            ))
            fig_dist.add_trace(go.Histogram(
                x=df_result[df_result["is_fraud_bool"]]["detection_score"],
                name="Fraud", marker_color="rgba(239,68,68,0.7)", nbinsx=20,
            ))
            fig_dist.add_vline(x=ms, line_color=COLORS["accent_gold"], line_dash="dash",
                               annotation_text=f"Threshold ({ms})", annotation_position="top right")
            apply_theme(fig_dist, height=280, barmode="overlay",
                                   legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#0E3A6E", orientation="h", y=-0.2))
            st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("🚨  FLAGGED TRANSACTIONS")

        display_cols = ["transaction_id","date","time","customer_name","bank","transaction_type",
                        "amount_naira","detection_score","detection_label","rules_text","is_fraud","fraud_type"]
        
        show_df = detected[display_cols].copy()
        show_df = show_df.rename(columns={
            "transaction_id":"TXN ID","date":"Date","time":"Time","customer_name":"Customer",
            "bank":"Bank","transaction_type":"Type","amount_naira":"Amount (₦)",
            "detection_score":"Score","detection_label":"Risk","rules_text":"Rules Triggered",
            "is_fraud":"Actual","fraud_type":"Fraud Type"
        })
        show_df["Amount (₦)"] = show_df["Amount (₦)"].apply(lambda x: f"₦{x:,.2f}")
        
        st.dataframe(show_df.sort_values("Score", ascending=False),
                     use_container_width=True, height=400)
        
        # Download
        csv_export = detected[display_cols].to_csv(index=False)
        st.download_button("⬇  EXPORT FRAUD REPORT (CSV)", csv_export,
                           "sentinel_fraud_report.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "analytics":
    
    st.markdown("""
    <div class="system-banner">
        <div class="banner-title">📊 Advanced Analytics & Intelligence</div>
        <div class="banner-subtitle">MULTI-DIMENSIONAL FRAUD PATTERN ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["  TEMPORAL  ", "  GEOGRAPHIC  ", "  AMOUNTS  ", "  BEHAVIOUR  "])

    with tab1:
        section_header("📅  WEEKLY FRAUD TREND")
        weekly = df_full.groupby(["week","is_fraud_bool"]).size().reset_index(name="count")
        weekly["label"] = weekly["is_fraud_bool"].map({True:"Fraud",False:"Normal"})
        fig = px.line(weekly, x="week", y="count", color="label",
                      color_discrete_map={"Fraud":"#EF4444","Normal":"#0EA5E9"},
                      markers=True, labels={"week":"Week Number","count":"Transactions"})
        apply_theme(fig, height=300)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        tc1, tc2 = st.columns(2)
        with tc1:
            section_header("📅  FRAUD BY DAY OF WEEK")
            dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            dow = df_full.groupby("day_of_week").agg(
                total=("transaction_id","count"),fraud=("is_fraud_bool","sum")).reset_index()
            dow["rate"] = dow["fraud"]/dow["total"]*100
            dow["day_of_week"] = pd.Categorical(dow["day_of_week"], categories=dow_order, ordered=True)
            dow = dow.sort_values("day_of_week")
            fig2 = px.bar(dow, x="day_of_week", y="rate",
                          color="rate", color_continuous_scale=["#0EA5E9","#EF4444"],
                          labels={"day_of_week":"Day","rate":"Fraud Rate %"})
            apply_theme(fig2, height=250, coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        
        with tc2:
            section_header("🌙  FRAUD HEAT MAP — HOUR vs DAY")
            heatmap_data = df_full[df_full["is_fraud_bool"]].groupby(["day_of_week","hour"]).size().reset_index(name="count")
            heatmap_pivot = heatmap_data.pivot(index="day_of_week", columns="hour", values="count").fillna(0)
            # Reorder rows
            ordered_days = [d for d in dow_order if d in heatmap_pivot.index]
            heatmap_pivot = heatmap_pivot.reindex(ordered_days)
            fig3 = go.Figure(go.Heatmap(
                z=heatmap_pivot.values, x=heatmap_pivot.columns.tolist(),
                y=heatmap_pivot.index.tolist(),
                colorscale=[[0,"#071528"],[0.5,"#0EA5E9"],[1,"#EF4444"]],
                hovertemplate="Day: %{y}<br>Hour: %{x}:00<br>Fraud cases: %{z}<extra></extra>",
            ))
            apply_theme(fig3, height=250,
                               xaxis_title="Hour", yaxis_title="")
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with tab2:
        section_header("🗺️  FRAUD BY HOME STATE")
        state_data = df_full.groupby("home_state").agg(
            total=("transaction_id","count"),
            fraud=("is_fraud_bool","sum"),
            fraud_value=("amount_naira",lambda x: x[df_full.loc[x.index,"is_fraud_bool"]].sum())
        ).reset_index()
        state_data["fraud_rate"] = state_data["fraud"]/state_data["total"]*100

        fc1, fc2 = st.columns(2)
        with fc1:
            fig = px.bar(state_data.sort_values("fraud_rate",ascending=True),
                         y="home_state", x="fraud_rate", orientation="h",
                         color="fraud_rate",
                         color_continuous_scale=["#0EA5E9","#F59E0B","#EF4444"],
                         labels={"home_state":"State","fraud_rate":"Fraud Rate %"},
                         text=[f"{v:.1f}%" for v in state_data.sort_values("fraud_rate")["fraud_rate"]])
            apply_theme(fig, height=380, coloraxis_showscale=False)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        with fc2:
            fig2 = px.treemap(state_data, path=["home_state"], values="fraud",
                              color="fraud_rate",
                              color_continuous_scale=["#071528","#0EA5E9","#EF4444"],
                              labels={"fraud_rate":"Fraud Rate %","fraud":"Fraud Cases"})
            apply_theme(fig2, height=380)
            fig2.update_traces(textinfo="label+value")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with tab3:
        section_header("💰  AMOUNT ANALYSIS — FRAUD vs NORMAL")
        ac1, ac2 = st.columns(2)
        with ac1:
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=df_full[~df_full["is_fraud_bool"]]["amount_naira"].clip(upper=500000),
                name="Normal", marker_color=COLORS["accent_blue"],
                boxmean=True, jitter=0.1, pointpos=-1.8,
            ))
            fig.add_trace(go.Box(
                y=df_full[df_full["is_fraud_bool"]]["amount_naira"].clip(upper=2000000),
                name="Fraud", marker_color=COLORS["red_high"],
                boxmean=True,
            ))
            apply_theme(fig, height=350,
                              yaxis_title="Amount (₦)", title="Amount Distribution")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with ac2:
            bins = [0,5000,10000,50000,100000,500000,1000000,float("inf")]
            labels = ["<5K","5–10K","10–50K","50–100K","100–500K","500K–1M",">1M"]
            df_full["amount_band"] = pd.cut(df_full["amount_naira"], bins=bins, labels=labels)
            band_data = df_full.groupby(["amount_band","is_fraud_bool"]).size().reset_index(name="count")
            band_data["label"] = band_data["is_fraud_bool"].map({True:"Fraud",False:"Normal"})
            fig2 = px.bar(band_data, x="amount_band", y="count", color="label",
                          color_discrete_map={"Fraud":"#EF4444","Normal":"#0EA5E9"},
                          barmode="group", labels={"amount_band":"Amount Band","count":"Count"})
            apply_theme(fig2, height=350, title="Fraud by Amount Band")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with tab4:
        section_header("🔬  FRAUD TYPE & TRANSACTION TYPE MATRIX")
        bc1, bc2 = st.columns(2)
        with bc1:
            txn_fraud = df_full[df_full["is_fraud_bool"]].groupby(
                ["transaction_type","fraud_type"]).size().reset_index(name="count")
            fig = px.sunburst(txn_fraud, path=["transaction_type","fraud_type"],
                              values="count",
                              color_discrete_sequence=px.colors.qualitative.Dark24)
            apply_theme(fig, height=380,
                              title="Transaction Type → Fraud Type")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        with bc2:
            profile_data = df_full.groupby("customer_profile").agg(
                total=("transaction_id","count"),
                fraud=("is_fraud_bool","sum"),
                avg_amount=("amount_naira","mean")
            ).reset_index()
            profile_data["fraud_rate"] = profile_data["fraud"]/profile_data["total"]*100
            fig2 = px.scatter(profile_data, x="avg_amount", y="fraud_rate",
                              size="total", color="customer_profile", text="customer_profile",
                              color_discrete_sequence=["#0EA5E9","#22D3EE","#F59E0B","#EF4444"],
                              labels={"avg_amount":"Avg Transaction (₦)","fraud_rate":"Fraud Rate %"})
            apply_theme(fig2, height=380,
                               title="Profile: Avg Amount vs Fraud Rate")
            fig2.update_traces(textposition="top center")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "customer":
    
    st.markdown("""
    <div class="system-banner">
        <div class="banner-title">👤 Customer Intelligence</div>
        <div class="banner-subtitle">INDIVIDUAL ACCOUNT RISK PROFILING & TRANSACTION HISTORY</div>
    </div>
    """, unsafe_allow_html=True)

    # Customer selector
    customers_list = df_full.groupby(["customer_id","customer_name"]).agg(
        total=("transaction_id","count"),
        fraud_count=("is_fraud_bool","sum")
    ).reset_index()
    customers_list["display"] = customers_list["customer_name"] + " (" + customers_list["customer_id"] + ")"
    customers_list["fraud_rate"] = customers_list["fraud_count"] / customers_list["total"] * 100
    customers_list = customers_list.sort_values("fraud_rate", ascending=False)

    sel_customer = st.selectbox("SELECT CUSTOMER", options=customers_list["display"].tolist(),
                                index=0, placeholder="Search customer...")

    if sel_customer:
        cid = sel_customer.split("(")[-1].rstrip(")")
        cdf = df_full[df_full["customer_id"] == cid].copy()
        
        cust_info = cdf.iloc[0].to_dict()   # convert to plain dict — avoids numpy scalar issues
        # Ensure string fields are proper Python strings (not numpy types)
        for _k in ["account_number","card_last4","customer_id","customer_name",
                   "bank","card_type","home_state","customer_profile",
                   "transaction_type","fraud_type","fraud_reason"]:
            if _k in cust_info:
                cust_info[_k] = str(cust_info[_k])
        # Ensure numeric fields are proper Python floats
        for _k in ["daily_limit","typical_max_amount","balance_before","balance_after",
                   "amount_naira","daily_total_so_far","risk_score"]:
            if _k in cust_info:
                try:
                    cust_info[_k] = float(cust_info[_k])
                except (ValueError, TypeError):
                    cust_info[_k] = 0.0
        fraud_txns = cdf[cdf["is_fraud_bool"]]
        total_spent = cdf[cdf["transaction_type"].isin(["ATM Withdrawal","POS Purchase","Online Transfer","Online Purchase","Mobile Transfer"])]["amount_naira"].sum()

        # Customer header
        profile_color = {"low":"#22C55E","medium":"#0EA5E9","high":"#F59E0B","premium":"#8B5CF6"}.get(cust_info["customer_profile"],"#0EA5E9")
        st.markdown(f"""
        <div class="system-banner" style="padding:20px 28px;">
            <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;">
                <div style="display:flex;align-items:center;gap:16px;">
                    <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,{profile_color}22,{profile_color}44);
                         border:2px solid {profile_color};display:flex;align-items:center;justify-content:center;font-size:22px;">
                        👤
                    </div>
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;">{cust_info['customer_name']}</div>
                        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#94A3B8;">
                            {cust_info['customer_id']} &nbsp;·&nbsp; Acct: ****{str(cust_info['account_number'])[-4:]} 
                            &nbsp;·&nbsp; Card: ****{str(cust_info['card_last4'])}
                        </div>
                        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#94A3B8;margin-top:4px;">
                            {cust_info['bank']} &nbsp;·&nbsp; {cust_info['card_type']} &nbsp;·&nbsp; {cust_info['home_state']}
                        </div>
                    </div>
                </div>
                <div style="display:flex;gap:24px;">
                    <div style="text-align:center;">
                        <div style="font-family:'DM Mono',monospace;font-size:10px;color:#475569;">PROFILE</div>
                        <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:{profile_color};">{cust_info['customer_profile'].upper()}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-family:'DM Mono',monospace;font-size:10px;color:#475569;">FRAUD RATE</div>
                        <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#EF4444;">{len(fraud_txns)/len(cdf)*100:.1f}%</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-family:'DM Mono',monospace;font-size:10px;color:#475569;">TOTAL SPENT</div>
                        <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;">₦{total_spent/1000:.0f}K</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats row
        cs1,cs2,cs3,cs4 = st.columns(4)
        with cs1: st.markdown(metric_card("TRANSACTIONS", f"{len(cdf)}", "Q1 2026", "#0EA5E9"), unsafe_allow_html=True)
        with cs2: st.markdown(metric_card("FRAUD FLAGS", f"{len(fraud_txns)}", f"{len(fraud_txns)/len(cdf)*100:.1f}% of total", "#EF4444"), unsafe_allow_html=True)
        with cs3: st.markdown(metric_card("DAILY LIMIT", f"₦{cust_info['daily_limit']/1000:.0f}K", cust_info["customer_profile"], "#F59E0B"), unsafe_allow_html=True)
        with cs4: st.markdown(metric_card("TYPICAL MAX", f"₦{cust_info['typical_max_amount']:,.0f}", "per transaction", "#22D3EE"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        cc1, cc2 = st.columns([3,2])
        with cc1:
            section_header("📈  TRANSACTION TIMELINE")
            fig = go.Figure()
            normal = cdf[~cdf["is_fraud_bool"]]
            fraud_c = cdf[cdf["is_fraud_bool"]]
            
            fig.add_trace(go.Scatter(
                x=normal["date"], y=normal["amount_naira"],
                mode="markers", name="Normal",
                marker=dict(color="#0EA5E9", size=8, opacity=0.7),
                hovertemplate="%{x}: ₦%{y:,.0f}<extra>Normal</extra>"
            ))
            fig.add_trace(go.Scatter(
                x=fraud_c["date"], y=fraud_c["amount_naira"],
                mode="markers", name="Fraud",
                marker=dict(color="#EF4444", size=12, symbol="x",
                            line=dict(width=2, color="#EF4444")),
                hovertemplate="%{x}: ₦%{y:,.0f}<extra>FRAUD</extra>"
            ))
            fig.add_hline(y=cust_info["typical_max_amount"], line_dash="dash",
                          line_color=COLORS["accent_gold"], 
                          annotation_text="Typical Max", annotation_position="right")
            apply_theme(fig, height=300, yaxis_title="Amount (₦)")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with cc2:
            section_header("🕐  ACTIVITY BY HOUR")
            hour_cdf = cdf.groupby(["hour","is_fraud_bool"]).size().reset_index(name="count")
            hour_cdf["label"] = hour_cdf["is_fraud_bool"].map({True:"Fraud",False:"Normal"})
            fig2 = px.bar(hour_cdf, x="hour", y="count", color="label",
                          color_discrete_map={"Fraud":"#EF4444","Normal":"#0EA5E9"},
                          barmode="stack")
            apply_theme(fig2, height=300,
                               xaxis_title="Hour", yaxis_title="Transactions",
                               legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#0E3A6E", orientation="h",y=-0.3))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("📋  FULL TRANSACTION HISTORY")
        
        show_cdf = cdf[["transaction_id","date","time","transaction_type","amount_naira",
                         "atm_location","transaction_status","is_fraud","fraud_type","fraud_reason"]].copy()
        show_cdf["amount_naira"] = show_cdf["amount_naira"].apply(lambda x: f"₦{x:,.2f}")
        st.dataframe(show_cdf, use_container_width=True, height=300)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALERTS & REPORTS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "alerts":

    st.markdown("""
    <div class="system-banner">
        <div class="banner-title">📋 Alerts & Fraud Reports</div>
        <div class="banner-subtitle">ACTIVE FRAUD ALERTS · CASE MANAGEMENT · EXPORT CENTRE</div>
    </div>
    """, unsafe_allow_html=True)

    # Filter
    af1, af2, af3 = st.columns(3)
    with af1:
        fraud_type_filter = st.selectbox("FRAUD TYPE", ["All Types"] + sorted(df_full[df_full["is_fraud_bool"]]["fraud_type"].unique().tolist()))
    with af2:
        bank_filter = st.selectbox("BANK", ["All Banks"] + sorted(df_full["bank"].unique().tolist()))
    with af3:
        min_amount_filter = st.number_input("MIN AMOUNT (₦)", value=0, step=10000)

    # Apply
    alert_df = df_full[df_full["is_fraud_bool"]].copy()
    if fraud_type_filter != "All Types": alert_df = alert_df[alert_df["fraud_type"] == fraud_type_filter]
    if bank_filter != "All Banks":       alert_df = alert_df[alert_df["bank"] == bank_filter]
    if min_amount_filter > 0:            alert_df = alert_df[alert_df["amount_naira"] >= min_amount_filter]
    alert_df = alert_df.sort_values("risk_score", ascending=False)

    st.markdown(f"""
    <div class="info-box" style="margin-bottom:16px;">
        Showing <strong>{len(alert_df):,}</strong> fraud alerts matching your filters. 
        Total exposure: <strong>₦{alert_df['amount_naira'].sum()/1e6:.2f}M</strong>
    </div>
    """, unsafe_allow_html=True)

    # Priority alerts (Critical)
    critical_alerts = alert_df[alert_df["risk_score"] >= 85]
    if len(critical_alerts) > 0:
        section_header(f"🔴  CRITICAL ALERTS — {len(critical_alerts)} cases requiring immediate action")
        for _, row in critical_alerts.head(10).iterrows():
            st.markdown(f"""
            <div class="alert-toast">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                            <span class="risk-badge risk-critical">CRITICAL</span>
                            <span style="font-family:'DM Mono',monospace;font-size:11px;color:#94A3B8;">{row['transaction_id']}</span>
                            <span style="font-family:'DM Mono',monospace;font-size:11px;color:#475569;">{row['date']} {row['time']}</span>
                        </div>
                        <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;margin-bottom:4px;">
                            ₦{row['amount_naira']:,.2f} 
                            <span style="font-size:13px;color:#EF4444;font-family:'Space Grotesk';">— {row['fraud_type']}</span>
                        </div>
                        <div style="font-size:13px;color:#94A3B8;margin-bottom:6px;">
                            👤 {row['customer_name']} &nbsp;·&nbsp; {row['bank']} &nbsp;·&nbsp; {row['home_state']}
                        </div>
                        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#EF4444;">
                            ⚡ {row['fraud_reason']}
                        </div>
                        <div style="margin-top:10px;padding:8px 12px;background:rgba(0,0,0,0.3);border-radius:6px;font-size:12px;color:#94A3B8;">
                            <strong style="color:#F0F9FF;">ACTION REQUIRED:</strong> Block card immediately · Call customer · File SAR (Suspicious Activity Report) · Notify compliance officer
                        </div>
                    </div>
                    <div style="text-align:center;min-width:70px;">
                        <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#EF4444;">{row['risk_score']}</div>
                        <div style="font-family:'DM Mono',monospace;font-size:10px;color:#475569;">RISK</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("📊  ALL FRAUD ALERTS")

    show_alert = alert_df[["transaction_id","date","time","customer_name","bank",
                            "transaction_type","amount_naira","risk_score",
                            "fraud_type","fraud_reason","transaction_status"]].copy()
    show_alert["amount_naira"] = show_alert["amount_naira"].apply(lambda x: f"₦{x:,.2f}")
    st.dataframe(show_alert, use_container_width=True, height=400)

    # Export section
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("📥  EXPORT CENTRE")
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        csv1 = alert_df.to_csv(index=False)
        st.download_button("⬇  FRAUD ALERTS (CSV)", csv1, "sentinel_alerts.csv", "text/csv", use_container_width=True)
    with ec2:
        summary = {
            "Report":"Sentinel Fraud Report Q1 2026",
            "Total Transactions":len(df_full),
            "Total Fraud Cases":df_full["is_fraud_bool"].sum(),
            "Fraud Rate (%)": f"{df_full['is_fraud_bool'].mean()*100:.2f}%",
            "Total Fraud Value":f"₦{df_full[df_full['is_fraud_bool']]['amount_naira'].sum():,.2f}",
            "Most Common Fraud":df_full[df_full["is_fraud_bool"]]["fraud_type"].mode()[0],
            "Highest Risk Score":df_full["risk_score"].max(),
        }
        import json
        csv2 = pd.DataFrame([summary]).to_csv(index=False)
        st.download_button("⬇  SUMMARY REPORT (CSV)", csv2, "sentinel_summary.csv", "text/csv", use_container_width=True)
    with ec3:
        csv3 = df_full.to_csv(index=False)
        st.download_button("⬇  FULL DATASET (CSV)", csv3, "sentinel_full_dataset.csv", "text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ENGINE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "config":

    st.markdown("""
    <div class="system-banner">
        <div class="banner-title">⚙️ Detection Engine Configuration</div>
        <div class="banner-subtitle">RULE PARAMETERS · THRESHOLDS · SYSTEM REFERENCE</div>
    </div>
    """, unsafe_allow_html=True)

    ct1, ct2 = st.columns(2)
    
    with ct1:
        section_header("🔧  DETECTION RULES")
        rules_info = [
            ("Rule 1","Large Amount","amount_naira > typical_max × N","Flags transactions N× above the customer's personal spending baseline. Catches card drainers who maximise withdrawal size.","30 pts","#EF4444"),
            ("Rule 2","Unusual Hour","0 ≤ hour ≤ N","Flags transactions between midnight and N:00am. Fraudsters exploit the window when cardholders are asleep.","20 pts","#F97316"),
            ("Rule 3","Foreign Location","'FOREIGN' in atm_location","Flags card use in a different state from the customer's registered home state. Key card-cloning indicator.","30 pts","#F59E0B"),
            ("Rule 4","Daily Limit Breach","daily_total_so_far > daily_limit","Flags when cumulative daily spend exceeds the bank-set daily limit. Catches systematic draining attacks.","25 pts","#EAB308"),
            ("Rule 5","Micro-Transaction","amount < ₦500","Flags tiny ATM or POS transactions. Fraudsters test stolen cards with small amounts before making large withdrawals.","15 pts","#22D3EE"),
            ("Rule 6","Near-Zero Balance","balance_after < ₦500","Flags transactions that leave the account near empty. Indicates a card-draining attack in progress.","10 pts","#8B5CF6"),
        ]
        for rule, name, condition, desc, pts, color in rules_info:
            st.markdown(f"""
            <div class="alert-card" style="--alert-color:{color};margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                            <span class="risk-badge" style="background:{color}22;color:{color};border-color:{color}44;">{rule}</span>
                            <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:14px;">{name}</span>
                        </div>
                        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#22D3EE;margin-bottom:6px;">{condition}</div>
                        <div style="font-size:12px;color:#94A3B8;">{desc}</div>
                    </div>
                    <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:{color};min-width:50px;text-align:right;">{pts}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with ct2:
        section_header("📊  SCORING MODEL")
        st.markdown("""
        <div class="info-box" style="margin-bottom:16px;">
            Each rule contributes a weighted score (0–100). The total score determines the risk classification.
            Multiple rules firing simultaneously multiply the overall confidence.
        </div>
        """, unsafe_allow_html=True)
        
        score_levels = [
            ("CRITICAL", "85 – 100", "#EF4444", "BLOCK CARD · CALL CUSTOMER · FILE SAR · NOTIFY COMPLIANCE"),
            ("HIGH",     "70 – 84",  "#F97316", "TEMPORARY HOLD · ANALYST REVIEW · SMS ALERT TO CUSTOMER"),
            ("MEDIUM",   "50 – 69",  "#EAB308", "FLAG FOR REVIEW · SEND NOTIFICATION · LOG INCIDENT"),
            ("LOW",      "25 – 49",  "#22C55E", "LOG AND MONITOR · NO IMMEDIATE ACTION REQUIRED"),
            ("CLEAR",    "0 – 24",   "#0EA5E9", "NORMAL TRANSACTION · CLEARED"),
        ]
        for level, score_range, color, action in score_levels:
            st.markdown(f"""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-left:4px solid {color};
                 border-radius:8px;padding:14px 18px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span class="risk-badge" style="background:{color}22;color:{color};border-color:{color}44;">{level}</span>
                        <span style="font-family:'DM Mono',monospace;font-size:11px;color:#94A3B8;margin-left:10px;">Score: {score_range}</span>
                        <div style="font-size:12px;color:#475569;margin-top:6px;font-family:'DM Mono',monospace;">{action}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("📋  DATASET REFERENCE")
        col_ref = {
            "transaction_id": "Unique transaction identifier (TXN0000001...)",
            "datetime": "Full timestamp YYYY-MM-DD HH:MM:SS",
            "amount_naira": "Transaction amount in Nigerian Naira (₦)",
            "typical_max_amount": "Customer's normal per-transaction maximum",
            "daily_limit": "Bank-set daily spending cap for this customer",
            "daily_total_so_far": "Running daily total at time of this transaction",
            "risk_score": "Ground truth risk score (0-100) assigned during generation",
            "is_fraud": "Ground truth fraud label: YES or NO",
            "fraud_type": "Category of fraud (Card Cloning, Skimming, SIM Swap, etc.)",
            "detection_score": "Score computed by SENTINEL rules engine",
        }
        for col, desc in col_ref.items():
            st.markdown(f"""
            <div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid var(--border);">
                <div style="font-family:'DM Mono',monospace;font-size:12px;color:#22D3EE;min-width:200px;">{col}</div>
                <div style="font-size:12px;color:#94A3B8;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
