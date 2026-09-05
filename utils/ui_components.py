"""
Shared UI design system for the Helmet Compliance Monitoring dashboard.

This module contains only presentation logic (CSS + small HTML component
helpers). It does not touch detection, database, or model code, so it is
safe to import from any page without affecting existing functionality.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
COLORS = {
    "bg": "#0B0F17",
    "surface": "#111826",
    "surface_alt": "#161F2E",
    "border": "#232B3B",
    "text": "#E6E9EF",
    "text_muted": "#8B95A7",
    "safe": "#22C55E",
    "safe_bg": "rgba(34, 197, 94, 0.12)",
    "violation": "#EF4444",
    "violation_bg": "rgba(239, 68, 68, 0.12)",
    "warning": "#F59E0B",
    "warning_bg": "rgba(245, 158, 11, 0.12)",
    "info": "#38BDF8",
    "info_bg": "rgba(56, 189, 248, 0.12)",
}


def inject_global_css():
    """Injects the shared stylesheet. Call once near the top of every page."""
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: -apple-system, "Segoe UI", Roboto, Inter, sans-serif;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }}

        #MainMenu, footer, header[data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['surface']};
            border-right: 1px solid {COLORS['border']};
        }}
        section[data-testid="stSidebar"] .block-container {{
            padding-top: 1.5rem;
        }}

        /* Buttons */
        .stButton > button, .stDownloadButton > button {{
            background-color: {COLORS['surface_alt']};
            color: {COLORS['text']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            font-weight: 500;
            padding: 0.5rem 1rem;
            transition: border-color 0.15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: {COLORS['info']};
            color: {COLORS['info']};
        }}
        .stButton > button[kind="primary"] {{
            background-color: {COLORS['info']};
            color: #05131F;
            border: none;
        }}

        /* File uploader */
        [data-testid="stFileUploaderDropzone"] {{
            background-color: {COLORS['surface']};
            border: 1.5px dashed {COLORS['border']};
            border-radius: 12px;
        }}
        [data-testid="stFileUploaderDropzone"]:hover {{
            border-color: {COLORS['info']};
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            border-bottom: 1px solid {COLORS['border']};
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {COLORS['text_muted']};
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            color: {COLORS['info']} !important;
        }}

        /* Expander */
        details {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
        }}

        /* Dataframe / table */
        [data-testid="stDataFrame"] {{
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            overflow: hidden;
        }}

        hr {{
            border-color: {COLORS['border']};
        }}

        /* Custom component classes */
        .app-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            padding-bottom: 1.25rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid {COLORS['border']};
        }}
        .app-header h1 {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {COLORS['text']};
            margin: 0;
        }}
        .app-header p {{
            color: {COLORS['text_muted']};
            margin: 0.25rem 0 0 0;
            font-size: 0.92rem;
        }}
        .status-pill-row {{
            display: flex;
            gap: 0.6rem;
        }}
        .status-pill {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 999px;
            padding: 0.35rem 0.8rem;
            font-size: 0.8rem;
            color: {COLORS['text_muted']};
            white-space: nowrap;
        }}
        .status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }}

        .section-header {{
            font-size: 1.05rem;
            font-weight: 600;
            color: {COLORS['text']};
            margin: 1.75rem 0 0.75rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .kpi-card {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1.1rem 1.25rem;
            height: 100%;
        }}
        .kpi-card .kpi-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.6rem;
        }}
        .kpi-card .kpi-icon {{
            font-size: 1.1rem;
            opacity: 0.85;
        }}
        .kpi-card .kpi-label {{
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: {COLORS['text_muted']};
        }}
        .kpi-card .kpi-value {{
            font-size: 1.9rem;
            font-weight: 700;
            color: {COLORS['text']};
            line-height: 1.1;
        }}
        .kpi-card .kpi-sub {{
            font-size: 0.78rem;
            color: {COLORS['text_muted']};
            margin-top: 0.35rem;
        }}

        .result-card {{
            border-radius: 12px;
            border: 1px solid {COLORS['border']};
            padding: 1rem 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .result-card.safe {{
            background-color: {COLORS['safe_bg']};
            border-color: rgba(34, 197, 94, 0.35);
        }}
        .result-card.violation {{
            background-color: {COLORS['violation_bg']};
            border-color: rgba(239, 68, 68, 0.35);
        }}
        .result-card .result-icon {{
            font-size: 1.5rem;
        }}
        .result-card .result-title {{
            font-weight: 700;
            font-size: 1rem;
            color: {COLORS['text']};
        }}
        .result-card .result-sub {{
            font-size: 0.82rem;
            color: {COLORS['text_muted']};
            margin-top: 0.15rem;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge.safe {{ background-color: {COLORS['safe_bg']}; color: {COLORS['safe']}; }}
        .badge.violation {{ background-color: {COLORS['violation_bg']}; color: {COLORS['violation']}; }}
        .badge.warning {{ background-color: {COLORS['warning_bg']}; color: {COLORS['warning']}; }}
        .badge.info {{ background-color: {COLORS['info_bg']}; color: {COLORS['info']}; }}

        .empty-state {{
            text-align: center;
            padding: 3rem 1rem;
            color: {COLORS['text_muted']};
            border: 1px dashed {COLORS['border']};
            border-radius: 12px;
            background-color: {COLORS['surface']};
        }}
        .empty-state .empty-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
            opacity: 0.7;
        }}

        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.25rem 0 1.1rem 0;
            border-bottom: 1px solid {COLORS['border']};
            margin-bottom: 1rem;
        }}
        .sidebar-brand .brand-icon {{
            font-size: 1.5rem;
        }}
        .sidebar-brand .brand-title {{
            font-size: 1.0rem;
            font-weight: 700;
            color: {COLORS['text']};
            line-height: 1.1;
        }}
        .sidebar-brand .brand-sub {{
            font-size: 0.72rem;
            color: {COLORS['text_muted']};
        }}
        .sidebar-footer {{
            border-top: 1px solid {COLORS['border']};
            padding-top: 0.9rem;
            margin-top: 1.2rem;
            font-size: 0.78rem;
            color: {COLORS['text_muted']};
        }}
        .sidebar-footer .footer-status {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            margin-top: 0.3rem;
            color: {COLORS['safe']};
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    """Logo + product name block at the top of the sidebar."""
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="brand-icon">🛡️</div>
            <div>
                <div class="brand-title">Helmet Compliance</div>
                <div class="brand-sub">AI Safety Monitoring</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_footer(model_ready: bool = True):
    """System status block pinned at the bottom of the sidebar."""
    dot_color = COLORS["safe"] if model_ready else COLORS["violation"]
    status_text = "System Online" if model_ready else "Model Unavailable"
    st.sidebar.markdown(
        f"""
        <div class="sidebar-footer">
            AI Safety Monitoring
            <div class="footer-status">
                <span class="status-dot" style="background-color:{dot_color};"></span>
                {status_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str, model_ready: bool = True):
    """Top header with title, subtitle, and live system status pills."""
    dot_color = COLORS["safe"] if model_ready else COLORS["violation"]
    system_text = "System Online" if model_ready else "System Offline"
    model_text = "AI Model Active" if model_ready else "AI Model Unavailable"
    st.markdown(
        f"""
        <div class="app-header">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            <div class="status-pill-row">
                <div class="status-pill">
                    <span class="status-dot" style="background-color:{dot_color};"></span>
                    {system_text}
                </div>
                <div class="status-pill">
                    <span class="status-dot" style="background-color:{COLORS['info']};"></span>
                    {model_text}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(icon: str, text: str):
    st.markdown(
        f'<div class="section-header">{icon} {text}</div>',
        unsafe_allow_html=True,
    )


def render_kpi_card(icon: str, label: str, value: str, sub: str = "", accent: str = "info"):
    """A single KPI metric card. `accent` picks the small top-right icon color."""
    accent_color = COLORS.get(accent, COLORS["info"])
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">{label}</div>
                <div class="kpi-icon" style="color:{accent_color};">{icon}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(is_safe: bool, title: str, subtitle: str = ""):
    """Large pass/fail result banner shown after a detection runs."""
    css_class = "safe" if is_safe else "violation"
    icon = "✅" if is_safe else "⚠️"
    st.markdown(
        f"""
        <div class="result-card {css_class}">
            <div class="result-icon">{icon}</div>
            <div>
                <div class="result-title">{title}</div>
                <div class="result-sub">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str, kind: str = "info"):
    """Small inline badge, e.g. for table cells. kind: safe|violation|warning|info"""
    return f'<span class="badge {kind}">{text}</span>'


def empty_state(icon: str, text: str):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-icon">{icon}</div>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
