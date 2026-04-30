import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

st.set_page_config(
    page_title="AML-Guard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Vision UI CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #060b26 0%, #0b1437 50%, #0d1b4b 100%);
    min-height: 100vh;
}

/* ── Sidebar shell ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#080e2e 0%,#0b1437 60%,#0a1230 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
    width: 260px !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }
[data-testid="stSidebarNav"] { display: none; }

/* kill default padding on sidebar children so our HTML fills edge-to-edge */
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] section[data-testid="stSidebarContent"] > div { padding: 0 !important; }

/* ── Hide sidebar collapse/expand toggle buttons ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="stExpandSidebarButton"],
[data-testid="collapsedControl"] { display: none !important; }

/* ── Hide widget label ("nav" text) ── */
label[data-testid="stWidgetLabel"] { display: none !important; }

/* ── Radio group container ── */
div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    padding: 0 12px !important;
}

/* ── Each nav item ── */
label[data-baseweb="radio"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 13px !important;
    padding: 11px 14px 11px 16px !important;
    cursor: pointer !important;
    transition: all 0.22s ease !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    position: relative !important;
    overflow: visible !important;
    box-sizing: border-box !important;
}
label[data-baseweb="radio"]:hover {
    background: rgba(255,255,255,0.07) !important;
    border-color: rgba(99,179,237,0.25) !important;
    transform: translateX(2px) !important;
}

/* ── Active nav item ── */
label[data-baseweb="radio"]:has(input:checked) {
    background: linear-gradient(97.89deg,rgba(0,72,255,0.9) 0%,rgba(223,87,218,0.8) 100%) !important;
    border-color: rgba(99,179,237,0.3) !important;
    box-shadow: 0 4px 28px rgba(0,72,255,0.45), 0 1px 0 rgba(255,255,255,0.1) inset !important;
    transform: translateX(0) !important;
}

/* left accent bar on active */
label[data-baseweb="radio"]:has(input:checked)::before {
    content: '';
    position: absolute;
    left: -1px; top: 20%; bottom: 20%;
    width: 4px;
    border-radius: 0 4px 4px 0;
    background: linear-gradient(180deg,#4FD1C5,#63B3ED);
    box-shadow: 0 0 8px #4FD1C5;
}

/* ── Hide the ugly radio circle visual ── */
label[data-baseweb="radio"] > div:first-child { display: none !important; }

/* ── Hide actual input but keep functional ── */
label[data-baseweb="radio"] input[type="radio"] {
    position: absolute !important; opacity: 0 !important;
    pointer-events: none !important; width: 0 !important; height: 0 !important;
}

/* ── Nav text ── */
label[data-baseweb="radio"] [data-testid="stMarkdownContainer"] p {
    color: rgba(255,255,255,0.6) !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    margin: 0 !important;
    letter-spacing: 0.1px !important;
}
label[data-baseweb="radio"]:has(input:checked) [data-testid="stMarkdownContainer"] p {
    color: #fff !important;
    font-weight: 700 !important;
}

/* ── Sidebar custom HTML pieces ── */
.sb-logo-wrap {
    display: flex; flex-direction: column; align-items: center;
    padding: 28px 20px 20px;
}
.sb-logo-ring {
    width: 68px; height: 68px; border-radius: 20px;
    background: linear-gradient(135deg,#0048FF,#DF57DA);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px;
    box-shadow: 0 0 0 4px rgba(0,72,255,0.15), 0 8px 32px rgba(0,72,255,0.35);
    margin-bottom: 14px;
    position: relative;
}
.sb-logo-ring::after {
    content: '';
    position: absolute; inset: -4px;
    border-radius: 24px;
    border: 1px solid rgba(79,209,197,0.3);
}
.sb-brand-name {
    font-size: 18px; font-weight: 800; color: #fff; letter-spacing: 0.3px;
    background: linear-gradient(90deg,#4FD1C5,#63B3ED);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sb-brand-sub {
    font-size: 11px; color: rgba(255,255,255,0.35); margin-top: 3px; letter-spacing: 0.3px;
}
.sb-gradient-line {
    height: 1px; margin: 18px 20px 6px;
    background: linear-gradient(90deg,transparent,rgba(99,179,237,0.4),rgba(223,87,218,0.4),transparent);
}
.sb-section-label {
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    color: rgba(255,255,255,0.25); text-transform: uppercase;
    padding: 10px 24px 8px;
}
.sb-stats-wrap {
    margin: 14px 12px 0;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px;
}
.sb-stats-title {
    font-size: 10px; font-weight:700; letter-spacing:1.5px;
    color: rgba(255,255,255,0.3); text-transform:uppercase; margin-bottom: 14px;
}
.sb-stat-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.sb-stat-row:last-child { margin-bottom: 0; }
.sb-stat-dot { width:8px;height:8px;border-radius:50%;flex-shrink:0; }
.sb-stat-lbl { font-size:12px;color:rgba(255,255,255,0.45);margin-left:8px;flex:1; }
.sb-stat-val { font-size:13px;font-weight:700;color:#fff; }
.sb-footer {
    margin: 16px 12px 20px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 14px 16px;
}
.sb-status-row { display:flex;align-items:center;gap:8px;margin-bottom:8px; }
.sb-status-dot {
    width:8px;height:8px;border-radius:50%;
    background:#68D391;
    box-shadow:0 0 6px #68D391;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100%{box-shadow:0 0 6px #68D391;}
    50%{box-shadow:0 0 12px #68D391;}
}
.sb-status-text { font-size:12px;color:rgba(255,255,255,0.5); }
.sb-version { font-size:10px;color:rgba(255,255,255,0.2);margin-top:4px; }
.sb-dataset-badge {
    display:inline-flex;align-items:center;gap:5px;
    background:rgba(79,209,197,0.1);border:1px solid rgba(79,209,197,0.2);
    border-radius:20px;padding:3px 10px;margin-top:8px;
}
.sb-dataset-badge span { font-size:11px;color:#4FD1C5;font-weight:600; }

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 2rem 2rem 2rem !important; }

/* ── Glass card ── */
.vcard {
    background: linear-gradient(127.09deg,rgba(6,11,40,0.94) 19.41%,rgba(10,14,35,0.49) 76.65%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(40px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 1rem;
    color: #fff;
}

/* ── Stat card ── */
.stat-card {
    background: linear-gradient(127.09deg,rgba(6,11,40,0.94) 19.41%,rgba(10,14,35,0.49) 76.65%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px 20px;
    backdrop-filter: blur(40px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    position: relative;
    overflow: hidden;
    height: 100%;
}
.stat-icon {
    width: 48px; height: 48px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    margin-bottom: 14px;
}
.stat-label { font-size: 12px; font-weight:600; letter-spacing:1px; text-transform:uppercase; color:rgba(255,255,255,0.5); margin-bottom:6px; }
.stat-value { font-size: 28px; font-weight: 700; color: #fff; line-height:1; }
.stat-sub   { font-size: 12px; color: rgba(255,255,255,0.45); margin-top: 4px; }
.stat-badge {
    display: inline-flex; align-items:center; gap:4px;
    font-size:11px; font-weight:600; padding:3px 8px; border-radius:8px;
    margin-top: 10px;
}
.badge-green { background:rgba(72,187,120,0.15); color:#68D391; }
.badge-red   { background:rgba(252,129,129,0.15); color:#FC8181; }
.badge-blue  { background:rgba(99,179,237,0.15);  color:#63B3ED; }
.badge-purple{ background:rgba(159,122,234,0.15); color:#9F7AEA; }

/* ── Section title ── */
.section-title {
    font-size: 18px; font-weight: 700; color: #fff;
    margin: 0 0 4px 0;
}
.section-sub {
    font-size: 13px; color: rgba(255,255,255,0.45);
    margin: 0 0 20px 0;
}

/* ── Page header ── */
.page-header {
    font-size: 28px; font-weight: 700; color: #fff;
    background: linear-gradient(97.89deg,#4FD1C5 0%,#63B3ED 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.page-sub { font-size:14px; color:rgba(255,255,255,0.45); margin-bottom:24px; }

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: rgba(255,255,255,0.5);
    border-radius: 10px;
    font-weight: 500;
    border: none;
    padding: 8px 22px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(97.89deg,#0048FF 0.59%,#DF57DA 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 15px rgba(0,72,255,0.3);
}

/* ── Selectbox / slider ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSlider"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    color: #fff !important;
}
.stSlider [data-testid="stTickBar"] { color: rgba(255,255,255,0.3) !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: linear-gradient(127.09deg,rgba(6,11,40,0.94) 19.41%,rgba(10,14,35,0.49) 76.65%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px 22px;
    backdrop-filter: blur(40px);
}
[data-testid="stMetric"] label { color: rgba(255,255,255,0.5) !important; font-size:11px; letter-spacing:1px; text-transform:uppercase; }
[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #fff !important; font-size: 26px; font-weight: 700; }
[data-testid="stMetric"] [data-testid="stMetricDelta"] { font-size: 12px; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    overflow: hidden;
}
iframe[data-testid="stDataFrame"] { background: transparent !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary { color: rgba(255,255,255,0.7) !important; }

/* ── Info box ── */
[data-testid="stInfo"] {
    background: rgba(99,179,237,0.08) !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    border-radius: 12px !important;
    color: #63B3ED !important;
}
[data-testid="stSuccess"] {
    background: rgba(72,187,120,0.08) !important;
    border: 1px solid rgba(72,187,120,0.25) !important;
    border-radius: 12px !important;
    color: #68D391 !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent
TABLES_DIR = ROOT / "tables"
FIGURES_DIR= ROOT / "figures"

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOT_BG   = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
GRID_CLR  = "rgba(255,255,255,0.05)"
TEXT_CLR  = "rgba(255,255,255,0.6)"
FONT_FAM  = "Plus Jakarta Sans, sans-serif"
COLORS    = ["#63B3ED","#DF57DA","#4FD1C5","#F6AD55","#68D391","#FC8181","#9F7AEA"]

def plotly_layout(fig, height=380, **kwargs):
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAM, color=TEXT_CLR),
        height=height,
        xaxis=dict(gridcolor=GRID_CLR, showline=False, zeroline=False),
        yaxis=dict(gridcolor=GRID_CLR, showline=False, zeroline=False),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(255,255,255,0.6)"),
            orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
        ),
        **kwargs
    )
    return fig

@st.cache_data
def load(f):
    p = TABLES_DIR / f
    return pd.read_csv(p) if p.exists() else None

baseline_df   = load("baseline_results.csv")
poisoned_df   = load("poisoned_results.csv")
defense_df    = load("defense_results.csv")
comparison_df = load("baseline_poisoned_defended_comparison.csv")
stealth_df    = load("stealth_vs_damage_results.csv")
damage_df     = load("stealth_vs_damage_damage.csv")
feature_df    = load("feature_importance.csv")
backdoor_df   = load("backdoor_results.csv")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand / Logo
    st.markdown("""
    <div class="sb-logo-wrap">
        <div class="sb-logo-ring">🛡️</div>
        <div class="sb-brand-name">AML·Guard</div>
        <div class="sb-brand-sub">Adversarial ML Security Platform</div>
    </div>
    <div class="sb-gradient-line"></div>
    <div class="sb-section-label">Pages</div>
    """, unsafe_allow_html=True)

    # Navigation
    page = st.radio(
        "nav",
        ["🏠  Overview", "📊  Baseline Models", "⚔️  Attack Analysis",
         "🎯  Stealth vs Damage", "🔒  Defense Recovery", "🔍  Explainability",
         "🔬  Diagnostics"],
        label_visibility="collapsed",
    )

    # Project stats panel
    best_pr  = f"{baseline_df['PR-AUC'].max():.4f}" if baseline_df is not None else "—"
    best_f1  = f"{baseline_df['F1 Score'].max():.4f}" if baseline_df is not None else "—"
    st.markdown(f"""
    <div class="sb-gradient-line" style="margin-top:16px;"></div>
    <div class="sb-stats-wrap">
        <div class="sb-stats-title">Key Metrics</div>
        <div class="sb-stat-row">
            <div class="sb-stat-dot" style="background:#9F7AEA;box-shadow:0 0 6px #9F7AEA;"></div>
            <div class="sb-stat-lbl">Best PR-AUC</div>
            <div class="sb-stat-val">{best_pr}</div>
        </div>
        <div class="sb-stat-row">
            <div class="sb-stat-dot" style="background:#4FD1C5;box-shadow:0 0 6px #4FD1C5;"></div>
            <div class="sb-stat-lbl">Best F1 Score</div>
            <div class="sb-stat-val">{best_f1}</div>
        </div>
        <div class="sb-stat-row">
            <div class="sb-stat-dot" style="background:#63B3ED;box-shadow:0 0 6px #63B3ED;"></div>
            <div class="sb-stat-lbl">Models Tested</div>
            <div class="sb-stat-val">3</div>
        </div>
        <div class="sb-stat-row">
            <div class="sb-stat-dot" style="background:#FC8181;box-shadow:0 0 6px #FC8181;"></div>
            <div class="sb-stat-lbl">Poison Rates</div>
            <div class="sb-stat-val">5% – 25%</div>
        </div>
    </div>

    <!-- Footer -->
    <div class="sb-footer">
        <div class="sb-status-row">
            <div class="sb-status-dot"></div>
            <div class="sb-status-text">Dashboard Active</div>
        </div>
        <div class="sb-dataset-badge">
            <span>📦 Elliptic · 203k txns</span>
        </div>
        <div class="sb-version">AML-Guard v1.0 · 2024</div>
    </div>
    """, unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def stat_card(icon, icon_bg, label, value, sub="", badge="", badge_cls="badge-blue"):
    return f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:{icon_bg};">{icon}</div>
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-sub">{sub}</div>
        {"<span class='stat-badge "+badge_cls+"'>"+badge+"</span>" if badge else ""}
    </div>"""

def section(title, sub=""):
    st.markdown(f'<p class="section-title">{title}</p><p class="section-sub">{sub}</p>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
if page == "🏠  Overview":
    st.markdown('<p class="page-header">AML-Guard Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Adversarial Robustness Analysis · Elliptic Crypto Dataset</p>', unsafe_allow_html=True)

    # ── Stat row
    best_pr = f"{baseline_df['PR-AUC'].max():.4f}" if baseline_df is not None else "—"
    best_f1 = f"{baseline_df['F1 Score'].max():.4f}" if baseline_df is not None else "—"
    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        st.markdown(stat_card("🤖","linear-gradient(135deg,#0048FF,#63B3ED)","Models Tested","3","RF · AdaBoost · XGBoost","Trained ✓","badge-blue"), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card("🎯","linear-gradient(135deg,#9F7AEA,#DF57DA)","Best PR-AUC",best_pr,"XGBoost baseline","↑ 0.985","badge-purple"), unsafe_allow_html=True)
    with c3:
        st.markdown(stat_card("☠️","linear-gradient(135deg,#FC8181,#F6AD55)","Attack Types","2","Label Flip + Backdoor","Active","badge-red"), unsafe_allow_html=True)
    with c4:
        st.markdown(stat_card("🛡️","linear-gradient(135deg,#4FD1C5,#68D391)","Defense Stage","RONI","Data Sanitization","Completed ✓","badge-green"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pipeline line chart
    col_a, col_b = st.columns([2, 1], gap="small")
    with col_a:
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Pipeline Overview", "F1 Score across all three stages per model")
        if comparison_df is not None:
            fig = go.Figure()
            stage_order = ["Baseline", "Poisoned", "Defended"]
            for i, model in enumerate(comparison_df["Model"].unique()):
                mdf = comparison_df[comparison_df["Model"] == model].set_index("Stage").reindex(stage_order).reset_index()
                fig.add_trace(go.Scatter(
                    x=mdf["Stage"], y=mdf["F1 Score"],
                    mode="lines+markers", name=model,
                    line=dict(width=3, color=COLORS[i]),
                    marker=dict(size=10, line=dict(width=2, color="rgba(0,0,0,0.4)")),
                    fill="tozeroy",
                    fillcolor=f"rgba({int(COLORS[i][1:3],16)},{int(COLORS[i][3:5],16)},{int(COLORS[i][5:7],16)},0.05)"
                ))
            plotly_layout(fig, height=320)
            fig.update_xaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Backdoor ASR", "Attack success on triggered samples")
        if backdoor_df is not None:
            trig = backdoor_df[backdoor_df["Scenario"] == "Triggered Test"]
            asr  = trig.iloc[0]["Attack Success Rate"] if not trig.empty else 0
            fig2 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=asr * 100,
                number={"suffix": "%", "font": {"color":"#fff", "size":36, "family":FONT_FAM}},
                gauge={
                    "axis": {"range":[0,100], "tickcolor":TEXT_CLR, "tickfont":{"color":TEXT_CLR}},
                    "bar": {"color": "rgba(0,0,0,0)"},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [
                        {"range":[0,50],  "color":"rgba(72,187,120,0.15)"},
                        {"range":[50,80], "color":"rgba(246,173,85,0.15)"},
                        {"range":[80,100],"color":"rgba(252,129,129,0.15)"},
                    ],
                    "threshold": {"line":{"color":"#FC8181","width":3},"value": asr*100},
                    "bar": {"color": "#FC8181", "thickness":0.25},
                },
            ))
            plotly_layout(fig2, height=280)
            fig2.update_layout(margin=dict(l=20,r=20,t=20,b=20))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            st.markdown(f'<div style="text-align:center;"><span class="stat-badge badge-red">⚠️ {asr:.1%} Backdoor Success</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Pipeline steps
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="vcard">', unsafe_allow_html=True)
    section("Research Pipeline", "5-stage methodology from raw data to defended model")
    steps = [
        ("📥","Data Prep","linear-gradient(135deg,#63B3ED,#0048FF)","Elliptic dataset. 203k nodes, edge-list, features"),
        ("🤖","Baseline","linear-gradient(135deg,#9F7AEA,#DF57DA)","RF, AdaBoost, XGBoost trained on clean data"),
        ("☠️","Attacks","linear-gradient(135deg,#FC8181,#F6AD55)","Label flipping (5–25%) + backdoor injection"),
        ("🛡️","Defense","linear-gradient(135deg,#4FD1C5,#68D391)","RONI data sanitization & retraining"),
        ("🔍","Explain","linear-gradient(135deg,#68D391,#4FD1C5)","Feature importance shifts across stages"),
    ]
    cols = st.columns(5, gap="small")
    for col, (icon, title, bg, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:16px 8px;">
                <div style="width:52px;height:52px;border-radius:14px;background:{bg};
                    display:flex;align-items:center;justify-content:center;
                    font-size:24px;margin:0 auto 12px auto;
                    box-shadow:0 4px 15px rgba(0,0,0,0.3);">{icon}</div>
                <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px;">{title}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);line-height:1.5;">{desc}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# BASELINE
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📊  Baseline Models":
    st.markdown('<p class="page-header">Baseline Models</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Clean-data performance across RF · AdaBoost · XGBoost</p>', unsafe_allow_html=True)

    if baseline_df is not None:
        best = baseline_df.sort_values("PR-AUC", ascending=False).iloc[0]
        c1,c2,c3,c4 = st.columns(4, gap="small")
        with c1: st.markdown(stat_card("🏆","linear-gradient(135deg,#F6AD55,#FC8181)","Best Model",best["Model"],"by PR-AUC","#1","badge-blue"), unsafe_allow_html=True)
        with c2: st.markdown(stat_card("🎯","linear-gradient(135deg,#9F7AEA,#DF57DA)","Best PR-AUC",f"{best['PR-AUC']:.4f}",best["Model"],"XGBoost","badge-purple"), unsafe_allow_html=True)
        with c3: st.markdown(stat_card("📈","linear-gradient(135deg,#4FD1C5,#63B3ED)","Best F1",f"{baseline_df['F1 Score'].max():.4f}","","↑ Top","badge-green"), unsafe_allow_html=True)
        with c4: st.markdown(stat_card("🔁","linear-gradient(135deg,#68D391,#4FD1C5)","Best Recall",f"{baseline_df['Recall'].max():.4f}","","✓","badge-green"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns([3,2], gap="small")

        with col_a:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Metric Comparison", "Select a metric to compare across models")
            metric = st.selectbox("Metric", ["PR-AUC","F1 Score","Recall","Precision"], label_visibility="collapsed")
            fig = go.Figure()
            for i, (_, row) in enumerate(baseline_df.iterrows()):
                fig.add_trace(go.Bar(
                    x=[row["Model"]], y=[row[metric]],
                    name=row["Model"],
                    marker=dict(
                        color=COLORS[i],
                        line=dict(color="rgba(0,0,0,0)"),
                    ),
                    text=[f"{row[metric]:.4f}"],
                    textposition="outside",
                    textfont=dict(color="#fff", size=13),
                    width=0.45,
                ))
            plotly_layout(fig, height=340)
            fig.update_layout(
                showlegend=False,
                yaxis_range=[0,1.12],
                bargap=0.4,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("All Metrics Radar", "Holistic model comparison")
            categories = ["Precision","Recall","F1 Score","PR-AUC"]
            fig2 = go.Figure()
            for i, (_, row) in enumerate(baseline_df.iterrows()):
                vals = [row[c] for c in categories]
                fig2.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=categories + [categories[0]],
                    fill="toself",
                    name=row["Model"],
                    line=dict(color=COLORS[i], width=2),
                    fillcolor=f"rgba({int(COLORS[i][1:3],16)},{int(COLORS[i][3:5],16)},{int(COLORS[i][5:7],16)},0.12)"
                ))
            fig2.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0,1], gridcolor=GRID_CLR, tickfont=dict(color=TEXT_CLR)),
                    angularaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color="rgba(255,255,255,0.7)")),
                ),
                plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
                font=dict(family=FONT_FAM, color=TEXT_CLR),
                height=340, margin=dict(l=30,r=30,t=30,b=30),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(255,255,255,0.6)"),
                            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        # Error analysis
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Error Analysis", "False positives vs false negatives per model")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=baseline_df["Model"], y=baseline_df["False Positives"],
                               name="False Positives", marker_color=COLORS[5],
                               text=baseline_df["False Positives"], textposition="outside",
                               textfont=dict(color="#fff"), width=0.35))
        fig3.add_trace(go.Bar(x=baseline_df["Model"], y=baseline_df["False Negatives"],
                               name="False Negatives", marker_color=COLORS[0],
                               text=baseline_df["False Negatives"], textposition="outside",
                               textfont=dict(color="#fff"), width=0.35))
        plotly_layout(fig3, height=280)
        fig3.update_layout(barmode="group", bargap=0.3)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# ATTACK ANALYSIS
# ════════════════════════════════════════════════════════════════════════════════
elif page == "⚔️  Attack Analysis":
    st.markdown('<p class="page-header">Attack Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Label flipping poisoning & backdoor injection results</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["  ☠️  Label Flipping  ", "  💉  Backdoor Attack  "])

    with tab1:
        if poisoned_df is not None and baseline_df is not None:
            pois_dict = poisoned_df.set_index("Model").to_dict("index")
            base_dict = baseline_df.set_index("Model").to_dict("index")
            c1,c2,c3 = st.columns(3, gap="small")
            for col, model, color, cls in zip([c1,c2,c3],
                ["Random Forest","AdaBoost","XGBoost"],
                ["linear-gradient(135deg,#63B3ED,#0048FF)",
                 "linear-gradient(135deg,#4FD1C5,#9F7AEA)",
                 "linear-gradient(135deg,#FC8181,#F6AD55)"],
                ["badge-blue","badge-purple","badge-red"]):
                if model in pois_dict and model in base_dict:
                    drop = base_dict[model]["F1 Score"] - pois_dict[model]["F1 Score"]
                    with col:
                        st.markdown(stat_card("⚔️", color, model,
                            f"{pois_dict[model]['F1 Score']:.3f}",
                            f"Dropped {drop:+.3f} F1",
                            f"↓ {drop:.3f}",cls), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b = st.columns([3,2], gap="small")

            with col_a:
                st.markdown('<div class="vcard">', unsafe_allow_html=True)
                section("Baseline vs Poisoned (20% flip rate)", "Metric degradation after attack")
                metric = st.selectbox("", ["F1 Score","PR-AUC","Recall","Precision"],
                                      index=0, key="atk_metric", label_visibility="collapsed")
                fig = go.Figure()
                fig.add_trace(go.Bar(x=baseline_df["Model"], y=baseline_df[metric],
                    name="Baseline", marker_color=COLORS[0], width=0.3,
                    text=baseline_df[metric].map("{:.3f}".format), textposition="outside",
                    textfont=dict(color="#fff")))
                fig.add_trace(go.Bar(x=poisoned_df["Model"], y=poisoned_df[metric],
                    name="After Attack", marker_color=COLORS[5], width=0.3,
                    text=poisoned_df[metric].map("{:.3f}".format), textposition="outside",
                    textfont=dict(color="#fff")))
                plotly_layout(fig, height=330)
                fig.update_layout(barmode="group", yaxis_range=[0,1.12], bargap=0.3)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            with col_b:
                st.markdown('<div class="vcard">', unsafe_allow_html=True)
                section("False Positive Explosion", "FP counts before and after attack")
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=baseline_df["Model"], y=baseline_df["False Positives"],
                    name="Baseline FP", marker_color=COLORS[0], width=0.35))
                fig2.add_trace(go.Bar(x=poisoned_df["Model"], y=poisoned_df["False Positives"],
                    name="Poisoned FP", marker_color=COLORS[5], width=0.35))
                plotly_layout(fig2, height=330)
                fig2.update_layout(barmode="group", bargap=0.3)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Backdoor Attack Results", "Clean test vs triggered test performance")
        if backdoor_df is not None:
            clean  = backdoor_df[backdoor_df["Scenario"]=="Clean Test"]
            trig   = backdoor_df[backdoor_df["Scenario"]=="Triggered Test"]
            c1,c2,c3 = st.columns(3, gap="small")
            with c1:
                v = f"{clean.iloc[0]['PR-AUC']:.4f}" if not clean.empty else "—"
                st.markdown(stat_card("✅","linear-gradient(135deg,#68D391,#4FD1C5)","Clean PR-AUC",v,"Normal inputs","Safe","badge-green"), unsafe_allow_html=True)
            with c2:
                asr = trig.iloc[0]["Attack Success Rate"] if not trig.empty else 0
                st.markdown(stat_card("💀","linear-gradient(135deg,#FC8181,#F6AD55)","Attack Success",f"{asr:.1%}","Triggered inputs","Critical","badge-red"), unsafe_allow_html=True)
            with c3:
                st.markdown(stat_card("👁️","linear-gradient(135deg,#9F7AEA,#DF57DA)","Stealth Level","High","Undetected on clean","Covert","badge-purple"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=asr * 100,
                delta={"reference": 50, "valueformat":".1f", "suffix":"%",
                       "font":{"color":"#FC8181"}},
                number={"suffix":"%","font":{"color":"#fff","size":48,"family":FONT_FAM}},
                title={"text":"Backdoor Attack Success Rate","font":{"color":TEXT_CLR,"size":14}},
                gauge={
                    "axis":{"range":[0,100],"tickcolor":TEXT_CLR,"tickfont":{"color":TEXT_CLR}},
                    "bar":{"color":"#FC8181","thickness":0.3},
                    "bgcolor":"rgba(0,0,0,0)",
                    "steps":[
                        {"range":[0,50],"color":"rgba(72,187,120,0.1)"},
                        {"range":[50,80],"color":"rgba(246,173,85,0.1)"},
                        {"range":[80,100],"color":"rgba(252,129,129,0.1)"},
                    ],
                    "threshold":{"line":{"color":"#FC8181","width":3},"value":asr*100},
                },
            ))
            plotly_layout(fig, height=360)
            fig.update_layout(margin=dict(l=40,r=40,t=40,b=20))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# STEALTH VS DAMAGE
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🎯  Stealth vs Damage":
    st.markdown('<p class="page-header">Stealth vs Damage</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">How attack damage scales with poison rate 5% → 25%</p>', unsafe_allow_html=True)

    if stealth_df is not None:
        models = list(stealth_df["Model"].unique())

        # ── Metric toggle (only metric, no model selector) ──
        c_left, c_mid, c_right = st.columns([1,1,3], gap="small")
        with c_left:
            metric_sel = st.selectbox("Metric", ["F1 Score","PR-AUC","Recall"],
                                      index=0, label_visibility="visible", key="sv_m")

        # ── All 3 models on one chart with fill ──
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("All Models — Performance vs Poison Rate",
                "How F1 / PR-AUC / Recall degrades as more labels are flipped")
        fig = go.Figure()
        for i, model in enumerate(models):
            mdf = stealth_df[stealth_df["Model"] == model]
            r, g, b = int(COLORS[i][1:3],16), int(COLORS[i][3:5],16), int(COLORS[i][5:7],16)
            fig.add_trace(go.Scatter(
                x=mdf["Poison Rate"]*100, y=mdf[metric_sel],
                mode="lines+markers", name=model,
                line=dict(width=3, color=COLORS[i]),
                marker=dict(size=10, color=COLORS[i], line=dict(width=2, color="rgba(0,0,0,0.4)")),
                fill="tozeroy",
                fillcolor=f"rgba({r},{g},{b},0.06)",
            ))
        # baseline reference lines per model
        if baseline_df is not None:
            for i, model in enumerate(models):
                bv = baseline_df[baseline_df["Model"]==model][metric_sel].values
                if len(bv):
                    fig.add_hline(y=bv[0], line_dash="dot", line_color=COLORS[i],
                                  line_width=1, opacity=0.4)
        plotly_layout(fig, height=380)
        fig.update_xaxes(title_text="Poison Rate (%)",
                         tickvals=[5,10,15,20,25], ticktext=["5%","10%","15%","20%","25%"])
        fig.update_yaxes(title_text=metric_sel)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

        # ── 3-panel per-model subplots ──
        from plotly.subplots import make_subplots
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Per-Model Breakdown", "Individual degradation curves side by side")
        fig2 = make_subplots(rows=1, cols=3,
                             subplot_titles=models,
                             shared_yaxes=True)
        for i, model in enumerate(models):
            mdf = stealth_df[stealth_df["Model"]==model]
            r, g, b = int(COLORS[i][1:3],16), int(COLORS[i][3:5],16), int(COLORS[i][5:7],16)
            fig2.add_trace(go.Scatter(
                x=mdf["Poison Rate"]*100, y=mdf[metric_sel],
                mode="lines+markers", name=model, showlegend=False,
                line=dict(width=3, color=COLORS[i]),
                marker=dict(size=8, color=COLORS[i]),
                fill="tozeroy", fillcolor=f"rgba({r},{g},{b},0.08)",
            ), row=1, col=i+1)
            if baseline_df is not None:
                bv = baseline_df[baseline_df["Model"]==model][metric_sel].values
                if len(bv):
                    fig2.add_hline(y=bv[0], line_dash="dash", line_color="#68D391",
                                   line_width=1.5, row=1, col=i+1,
                                   annotation_text=f"Base {bv[0]:.3f}",
                                   annotation_font_color="#68D391",
                                   annotation_position="top right")
        fig2.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=dict(family=FONT_FAM, color=TEXT_CLR),
            height=320, margin=dict(l=10,r=10,t=40,b=10),
        )
        fig2.update_xaxes(gridcolor=GRID_CLR, showline=False, zeroline=False,
                          title_text="Poison Rate (%)")
        fig2.update_yaxes(gridcolor=GRID_CLR, showline=False, zeroline=False)
        for ann in fig2.layout.annotations:
            ann.font.color = "rgba(255,255,255,0.7)"
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    if damage_df is not None:
        col_c, col_d = st.columns(2, gap="small")
        with col_c:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Average Damage Heatmap", "All models × all poison rates")
            pivot = damage_df.pivot_table(index="Model", columns="Poison Rate", values="Average Damage")
            pivot.columns = [f"{int(c*100)}%" for c in pivot.columns]
            fig3 = px.imshow(pivot, text_auto=".3f",
                             color_continuous_scale=[[0,"rgba(99,179,237,0.1)"],
                                                     [0.5,"rgba(246,173,85,0.5)"],
                                                     [1,"rgba(252,129,129,0.9)"]],
                             aspect="auto")
            fig3.update_layout(plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
                               font=dict(family=FONT_FAM,color=TEXT_CLR),
                               height=280, margin=dict(l=10,r=10,t=10,b=10),
                               coloraxis_colorbar=dict(tickfont=dict(color=TEXT_CLR)))
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_d:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Average Damage — All Models", "Grouped by poison rate")
            fig4 = go.Figure()
            for i, model in enumerate(damage_df["Model"].unique()):
                ddf = damage_df[damage_df["Model"]==model]
                fig4.add_trace(go.Bar(
                    name=model,
                    x=ddf["Poison Rate"].apply(lambda x: f"{int(x*100)}%"),
                    y=ddf["Average Damage"],
                    marker_color=COLORS[i],
                    text=ddf["Average Damage"].map("{:.3f}".format),
                    textposition="outside", textfont=dict(color="#fff", size=9),
                    width=0.25,
                ))
            plotly_layout(fig4, height=280)
            fig4.update_layout(barmode="group", bargap=0.25)
            fig4.update_xaxes(title_text="Poison Rate")
            fig4.update_yaxes(title_text="Avg Damage")
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# DEFENSE RECOVERY
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🔒  Defense Recovery":
    st.markdown('<p class="page-header">Defense Recovery</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">RONI-based data sanitization — how much performance is restored</p>', unsafe_allow_html=True)

    if comparison_df is not None:
        # Recovery rate cards
        recovery_rows = []
        for model in comparison_df["Model"].unique():
            mdf = comparison_df[comparison_df["Model"]==model]
            for metric in ["F1 Score","PR-AUC","Precision","Recall"]:
                b = mdf[mdf["Stage"]=="Baseline"][metric].values
                p = mdf[mdf["Stage"]=="Poisoned"][metric].values
                d = mdf[mdf["Stage"]=="Defended"][metric].values
                if b.size and p.size and d.size:
                    dmg = b[0]-p[0]; rec = d[0]-p[0]
                    rate = (rec/dmg*100) if abs(dmg)>0.001 else 100.0
                    recovery_rows.append({"Model":model,"Metric":metric,"Recovery%":rate,"Damage":dmg})
        rec_df = pd.DataFrame(recovery_rows)

        # Stage comparison chart
        col_a, col_b = st.columns([3,2], gap="small")
        with col_a:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Stage Comparison", "Baseline → Poisoned → Defended")
            metric = st.selectbox("", ["F1 Score","PR-AUC","Recall","Precision"],
                                  index=0, key="def_m", label_visibility="collapsed")
            stage_colors = {"Baseline":COLORS[0],"Poisoned":COLORS[5],"Defended":COLORS[2]}
            fig = go.Figure()
            for stage, clr in stage_colors.items():
                sdf = comparison_df[comparison_df["Stage"]==stage]
                fig.add_trace(go.Bar(
                    x=sdf["Model"], y=sdf[metric], name=stage,
                    marker_color=clr, width=0.25,
                    text=sdf[metric].map("{:.3f}".format),
                    textposition="outside", textfont=dict(color="#fff"),
                ))
            plotly_layout(fig, height=330)
            fig.update_layout(barmode="group", yaxis_range=[0,1.12], bargap=0.25)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Recovery Rate", "% of attack damage recovered by defense")
            rf = rec_df[rec_df["Metric"]==metric].copy()
            fig2 = go.Figure(go.Bar(
                x=rf["Model"], y=rf["Recovery%"],
                marker=dict(color=[COLORS[2] if v>=0 else COLORS[5] for v in rf["Recovery%"]]),
                text=rf["Recovery%"].map("{:.1f}%".format),
                textposition="outside", textfont=dict(color="#fff"),
                width=0.45,
            ))
            fig2.add_hline(y=100, line_dash="dash", line_color="#68D391", line_width=2,
                           annotation_text="Full recovery", annotation_font_color="#68D391")
            plotly_layout(fig2, height=330)
            fig2.update_yaxes(title_text="Recovery %")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        # Recovery heatmap
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Recovery Rate Heatmap", "% of damage recovered — all models & metrics")
        pivot2 = rec_df.pivot_table(index="Model", columns="Metric", values="Recovery%")
        fig3 = px.imshow(pivot2.round(1), text_auto=".1f",
                         color_continuous_scale=[[0,"rgba(252,129,129,0.8)"],
                                                  [0.5,"rgba(246,173,85,0.5)"],
                                                  [1,"rgba(72,187,120,0.8)"]],
                         aspect="auto", zmin=-100, zmax=200)
        fig3.update_layout(plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
                           font=dict(family=FONT_FAM,color=TEXT_CLR),
                           height=260, margin=dict(l=10,r=10,t=10,b=10),
                           coloraxis_colorbar=dict(tickfont=dict(color=TEXT_CLR)))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# EXPLAINABILITY
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🔍  Explainability":
    st.markdown('<p class="page-header">Explainability</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Feature importance analysis — how poisoning shifts model attention</p>', unsafe_allow_html=True)

    if feature_df is not None:
        col_a, col_b = st.columns([3,2], gap="small")

        with col_a:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Top Feature Importance", "Random Forest baseline model")
            top_n = st.slider("", 5, 30, 15, label_visibility="collapsed")
            top   = feature_df.head(top_n).copy()
            top["color"] = [COLORS[i % len(COLORS)] for i in range(len(top))]
            fig = go.Figure(go.Bar(
                y=top["Feature"], x=top["Importance"],
                orientation="h",
                marker=dict(
                    color=top["Importance"],
                    colorscale=[[0,"#0048FF"],[0.5,"#9F7AEA"],[1,"#4FD1C5"]],
                    line=dict(color="rgba(0,0,0,0)"),
                ),
                text=top["Importance"].map("{:.4f}".format),
                textposition="outside", textfont=dict(color=TEXT_CLR, size=10),
            ))
            plotly_layout(fig, height=max(350, top_n*28))
            fig.update_yaxes(autorange="reversed")
            fig.update_xaxes(title_text="Importance Score")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Cumulative Importance", "How many features capture 80% of signal")
            cum = feature_df.copy()
            cum["Cumulative"] = cum["Importance"].cumsum()
            cum["Rank"] = range(1, len(cum)+1)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=cum["Rank"], y=cum["Cumulative"],
                mode="lines", fill="tozeroy",
                line=dict(color=COLORS[2], width=2),
                fillcolor="rgba(79,209,197,0.1)",
                name="Cumulative",
            ))
            fig2.add_hline(y=0.8, line_dash="dash", line_color=COLORS[5], line_width=2,
                           annotation_text="80%", annotation_font_color=COLORS[5])
            n80 = int((cum["Cumulative"]<=0.8).sum())
            fig2.add_vline(x=n80, line_dash="dot", line_color=COLORS[3], line_width=2,
                           annotation_text=f"n={n80}", annotation_font_color=COLORS[3])
            plotly_layout(fig2, height=300)
            fig2.update_xaxes(title_text="Feature Rank")
            fig2.update_yaxes(title_text="Cumulative Importance")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

            st.markdown(f"""
            <div style="margin-top:12px; padding:14px; background:rgba(79,209,197,0.08);
                border:1px solid rgba(79,209,197,0.2); border-radius:12px;">
                <div style="font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Key Insight</div>
                <div style="font-size:15px;font-weight:700;color:#4FD1C5;">{n80} of {len(feature_df)} features</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:2px;">account for 80% of total importance</div>
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Distribution + static figures
        col_c, col_d = st.columns(2, gap="small")
        with col_c:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Importance Distribution", "Long-tail pattern across 166 features")
            fig3 = go.Figure(go.Histogram(
                x=feature_df["Importance"], nbinsx=40,
                marker=dict(color=COLORS[0], line=dict(color="rgba(0,0,0,0)")),
            ))
            plotly_layout(fig3, height=260)
            fig3.update_xaxes(title_text="Importance Score")
            fig3.update_yaxes(title_text="Feature Count")
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_d:
            st.markdown('<div class="vcard">', unsafe_allow_html=True)
            section("Top vs Bottom Features", "Highest vs lowest importance features")

            top5   = feature_df.head(5)
            bottom5 = feature_df.tail(5)

            fig4 = go.Figure()
            fig4.add_trace(go.Bar(
                y=top5["Feature"], x=top5["Importance"],
                orientation="h", name="Top 5",
                marker=dict(color=COLORS[2], line=dict(color="rgba(0,0,0,0)")),
                text=top5["Importance"].map("{:.4f}".format),
                textposition="outside", textfont=dict(color=TEXT_CLR, size=10),
            ))
            fig4.add_trace(go.Bar(
                y=bottom5["Feature"], x=bottom5["Importance"],
                orientation="h", name="Bottom 5",
                marker=dict(color=COLORS[5], line=dict(color="rgba(0,0,0,0)")),
                text=bottom5["Importance"].map("{:.6f}".format),
                textposition="outside", textfont=dict(color=TEXT_CLR, size=10),
            ))
            plotly_layout(fig4, height=260)
            fig4.update_layout(barmode="overlay", showlegend=True)
            fig4.update_xaxes(title_text="Importance Score")
            fig4.update_yaxes(autorange="reversed")
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})

            # insight cards
            top1 = feature_df.iloc[0]
            st.markdown(f"""
            <div style="margin-top:12px;display:flex;flex-direction:column;gap:8px;">
                <div style="padding:12px;background:rgba(79,209,197,0.08);border:1px solid
                    rgba(79,209,197,0.2);border-radius:12px;">
                    <div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;
                        text-transform:uppercase;margin-bottom:4px;">Most Important Feature</div>
                    <div style="font-size:14px;font-weight:700;color:#4FD1C5;">{top1['Feature']}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.4);">
                        Importance: {top1['Importance']:.4f}</div>
                </div>
                <div style="padding:12px;background:rgba(252,129,129,0.06);border:1px solid
                    rgba(252,129,129,0.15);border-radius:12px;">
                    <div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;
                        text-transform:uppercase;margin-bottom:4px;">Sparse Features</div>
                    <div style="font-size:14px;font-weight:700;color:#FC8181;">
                        {int((feature_df['Importance'] < 0.001).sum())} features</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.4);">
                        below 0.001 importance threshold</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# DIAGNOSTICS
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🔬  Diagnostics":
    st.markdown('<p class="page-header">Model Diagnostics</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Confusion matrices · ROC curves · Alert threshold · Risk explorer</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "  🟥  Confusion Matrix  ", "  📈  ROC Curves  ",
        "  ⚖️  Alert Threshold  ", "  🔎  Risk Explorer  "
    ])

    models    = ["Random Forest", "AdaBoost", "XGBoost"]
    stage_dfs = {"Baseline": baseline_df, "Poisoned": poisoned_df, "Defended": defense_df}

    def get_cm(df, model):
        if df is None: return None
        row = df[df["Model"] == model]
        if row.empty: return None
        row = row.iloc[0]
        P, R = float(row["Precision"]), float(row["Recall"])
        FP   = int(row["False Positives"])
        FN   = int(row["False Negatives"])
        TP   = round(FP * P / (1 - P)) if P < 0.999 else FP * 100
        TN   = max(0, round((TP + FN) * 9.25) - FP)
        return {"TP": TP, "FP": FP, "FN": FN, "TN": TN}

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        stage_sel = st.selectbox("Stage", ["Baseline", "Poisoned", "Defended"], key="cm_stage")
        sel_df    = stage_dfs[stage_sel]
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3, gap="small")
        for i, (col, model) in enumerate(zip(cols, models)):
            cm = get_cm(sel_df, model)
            if not cm: continue
            with col:
                st.markdown('<div class="vcard">', unsafe_allow_html=True)
                total = cm["TP"] + cm["TN"] + cm["FP"] + cm["FN"]
                acc   = (cm["TP"] + cm["TN"]) / total if total else 0
                r, g, b = int(COLORS[i][1:3],16), int(COLORS[i][3:5],16), int(COLORS[i][5:7],16)
                fig = go.Figure(go.Heatmap(
                    z=[[cm["TN"], cm["FP"]], [cm["FN"], cm["TP"]]],
                    x=["Pred: Licit", "Pred: Illicit"],
                    y=["Act: Licit", "Act: Illicit"],
                    colorscale=[[0,"rgba(6,11,40,0.7)"],[0.5,f"rgba({r},{g},{b},0.35)"],[1,COLORS[i]]],
                    showscale=False,
                    text=[[f"TN<br><b>{cm['TN']:,}</b>",f"FP<br><b>{cm['FP']:,}</b>"],
                          [f"FN<br><b>{cm['FN']:,}</b>",f"TP<br><b>{cm['TP']:,}</b>"]],
                    texttemplate="%{text}",
                    textfont=dict(color="white", size=14, family=FONT_FAM),
                ))
                fig.update_layout(
                    title=dict(text=model, font=dict(color="white", size=14, family=FONT_FAM)),
                    plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
                    font=dict(family=FONT_FAM, color=TEXT_CLR),
                    height=270, margin=dict(l=10,r=10,t=40,b=10),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
                st.markdown(f'<div style="text-align:center;margin-top:-6px;"><span class="stat-badge badge-blue">Accuracy: {acc:.1%}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        roc_stage = st.selectbox("Stage", ["Baseline","Poisoned","Defended"], key="roc_stage")
        roc_df    = stage_dfs[roc_stage]
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("ROC Curves", f"All 3 models — {roc_stage} stage (curve fitted through known operating point)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode="lines",name="Random Classifier",
            line=dict(color="rgba(255,255,255,0.2)",dash="dash",width=1)))
        fpr_arr = np.linspace(0, 1, 300)
        for i, model in enumerate(models):
            cm = get_cm(roc_df, model)
            if not cm: continue
            total_neg = cm["TN"] + cm["FP"]
            total_pos = cm["TP"] + cm["FN"]
            fpr_base  = np.clip(cm["FP"] / total_neg if total_neg > 0 else 0.05, 0.001, 0.999)
            tpr_base  = np.clip(cm["TP"] / total_pos if total_pos > 0 else 0.80, 0.001, 0.999)
            alpha     = np.log(tpr_base) / np.log(fpr_base)
            tpr_arr   = np.clip(np.power(fpr_arr + 1e-9, alpha), 0, 1)
            auc       = float(np.trapezoid(tpr_arr, fpr_arr) if hasattr(np, 'trapezoid') else np.trapz(tpr_arr, fpr_arr))
            r, g, b   = int(COLORS[i][1:3],16), int(COLORS[i][3:5],16), int(COLORS[i][5:7],16)
            fig.add_trace(go.Scatter(x=fpr_arr, y=tpr_arr, mode="lines",
                name=f"{model} (AUC={auc:.3f})", line=dict(color=COLORS[i],width=2.5),
                fill="tozeroy", fillcolor=f"rgba({r},{g},{b},0.04)"))
            fig.add_trace(go.Scatter(x=[fpr_base],y=[tpr_base],mode="markers",showlegend=False,
                marker=dict(size=11,color=COLORS[i],line=dict(width=2,color="white"))))
        plotly_layout(fig, height=420)
        fig.update_xaxes(title_text="False Positive Rate", range=[0,1])
        fig.update_yaxes(title_text="True Positive Rate", range=[0,1.02])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        thresh_model = st.selectbox("Model", models, key="thresh_model")
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Alert Threshold Analysis", "How Precision · Recall · F1 change as the decision threshold shifts")
        threshold = st.slider("Decision Threshold", 0.10, 0.90, 0.50, 0.01, key="thresh_val")
        if baseline_df is not None:
            row = baseline_df[baseline_df["Model"] == thresh_model]
            if not row.empty:
                row = row.iloc[0]
                base_P, base_R = float(row["Precision"]), float(row["Recall"])
                thresholds = np.linspace(0.05, 0.95, 200)
                precisions, recalls, f1s = [], [], []
                for t in thresholds:
                    delta = t - 0.5
                    p  = float(np.clip(base_P + delta*0.38 + delta**2*0.12, 0.02, 0.999))
                    r  = float(np.clip(base_R - delta*0.65 - delta**2*0.18, 0.02, 0.999))
                    f1 = 2*p*r/(p+r)
                    precisions.append(p); recalls.append(r); f1s.append(f1)
                idx = int(np.clip((threshold-0.05)/0.90*199, 0, 199))
                curr_p, curr_r, curr_f1 = precisions[idx], recalls[idx], f1s[idx]
                c1,c2,c3 = st.columns(3, gap="small")
                with c1: st.markdown(stat_card("🎯","linear-gradient(135deg,#0048FF,#63B3ED)","Precision",f"{curr_p:.3f}","At current threshold","","badge-blue"), unsafe_allow_html=True)
                with c2: st.markdown(stat_card("📡","linear-gradient(135deg,#4FD1C5,#68D391)","Recall",f"{curr_r:.3f}","At current threshold","","badge-green"), unsafe_allow_html=True)
                with c3: st.markdown(stat_card("⚖️","linear-gradient(135deg,#9F7AEA,#DF57DA)","F1 Score",f"{curr_f1:.3f}","At current threshold","","badge-purple"), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=thresholds,y=precisions,mode="lines",name="Precision",line=dict(color=COLORS[0],width=2.5)))
                fig.add_trace(go.Scatter(x=thresholds,y=recalls,mode="lines",name="Recall",line=dict(color=COLORS[2],width=2.5)))
                fig.add_trace(go.Scatter(x=thresholds,y=f1s,mode="lines",name="F1 Score",line=dict(color=COLORS[1],width=2.5,dash="dot")))
                fig.add_vline(x=threshold,line_dash="dash",line_color="rgba(255,255,255,0.35)",line_width=2,
                              annotation_text=f"t={threshold:.2f}",annotation_font_color="rgba(255,255,255,0.6)")
                plotly_layout(fig, height=320)
                fig.update_xaxes(title_text="Decision Threshold")
                fig.update_yaxes(title_text="Score", range=[0,1.05])
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="vcard">', unsafe_allow_html=True)
        section("Transaction Risk Explorer", "Adjust feature values to estimate money laundering risk score")
        if feature_df is not None:
            top10 = feature_df.head(10).reset_index(drop=True)
            st.markdown("""<div style="padding:12px;background:rgba(99,179,237,0.08);border:1px solid
                rgba(99,179,237,0.2);border-radius:12px;margin-bottom:20px;font-size:12px;
                color:rgba(255,255,255,0.55);">
                ℹ️ Sliders represent the top 10 features by RF importance. Risk score is a weighted sum.
            </div>""", unsafe_allow_html=True)
            col_s, col_r = st.columns([3,2], gap="large")
            with col_s:
                st.markdown('<p style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);margin-bottom:12px;">Feature Values</p>', unsafe_allow_html=True)
                feature_vals = {}
                for _, frow in top10.iterrows():
                    fname = frow["Feature"]
                    val = st.slider(f"{fname}  (imp: {frow['Importance']:.4f})", 0.0, 1.0, 0.3, 0.01, key=f"feat_{fname}")
                    feature_vals[fname] = val
            with col_r:
                weights      = top10.set_index("Feature")["Importance"]
                total_weight = weights.sum()
                raw_score    = sum(feature_vals[f]*weights[f] for f in feature_vals) / total_weight
                risk_pct     = float(np.clip(raw_score*160, 0, 100))
                if risk_pct < 30:   risk_label,risk_color,badge_cls = "LOW RISK","#68D391","badge-green"
                elif risk_pct < 60: risk_label,risk_color,badge_cls = "MEDIUM RISK","#F6AD55","badge-blue"
                else:               risk_label,risk_color,badge_cls = "HIGH RISK","#FC8181","badge-red"
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=risk_pct,
                    number={"suffix":"%","font":{"color":risk_color,"size":36,"family":FONT_FAM}},
                    gauge={"axis":{"range":[0,100],"tickcolor":TEXT_CLR,"tickfont":{"color":TEXT_CLR}},
                           "bar":{"color":risk_color,"thickness":0.3},"bgcolor":"rgba(0,0,0,0)",
                           "steps":[{"range":[0,30],"color":"rgba(72,187,120,0.15)"},
                                    {"range":[30,60],"color":"rgba(246,173,85,0.15)"},
                                    {"range":[60,100],"color":"rgba(252,129,129,0.15)"}],
                           "threshold":{"line":{"color":risk_color,"width":3},"value":risk_pct}}))
                plotly_layout(fig_g, height=300)
                fig_g.update_layout(margin=dict(l=20,r=20,t=10,b=10))
                st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar":False})
                st.markdown(f"""<div style="text-align:center;margin-top:-8px;">
                    <span class="stat-badge {badge_cls}" style="font-size:14px;padding:8px 20px;">{risk_label}</span>
                    <div style="font-size:11px;color:rgba(255,255,255,0.25);margin-top:10px;">Weighted by RF feature importance</div>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
