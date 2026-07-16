import streamlit as st
from streamlit_option_menu import option_menu

from utils.load_data import load_excel

from app_pages.upload_center import show_upload_center
from app_pages.dashboard_page import show_dashboard
from app_pages.vulnerabilities import show_vulnerabilities
from app_pages.analytics import show_analytics
from app_pages.remediation import show_remediation
from app_pages.scan_history import show_scan_history
from app_pages.reports import show_reports


# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="VAPT Vulnerability Management Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================================
# LOAD DATA
# ===================================================

executive_df, tracking_df, history_df, remediation_df = load_excel()

# ===================================================
# SIDEBAR
# ===================================================

with st.sidebar:

    st.title("🛡️ VAPT Dashboard")

    selected = option_menu(

        menu_title="Navigation",

        options=[
            "Report Ingestion",
            "Dashboard",
            "Vulnerability Manager",
            "Analytics",
            "Remediation",
            "Scan History",
            "Reports"
        ],

        icons=[
            "cloud-upload",
            "speedometer2",
            "bug",
            "bar-chart",
            "shield-check",
            "clock-history",
            "file-earmark-text"
        ],

        default_index=0

    )

# ===================================================
# PAGE ROUTING
# ===================================================

if selected == "Report Ingestion":

    show_upload_center()

elif selected == "Dashboard":

    show_dashboard(
        executive_df,
        tracking_df,
        history_df,
        remediation_df
    )

elif selected == "Vulnerability Manager":

    show_vulnerabilities(
        tracking_df
    )

elif selected == "Analytics":

    show_analytics(
        executive_df,
        tracking_df
    )

elif selected == "Remediation":

    show_remediation(
        remediation_df
    )

elif selected == "Scan History":

    show_scan_history(
        tracking_df
    )

elif selected == "Reports":

    show_reports(
        executive_df,
        tracking_df,
        history_df,
        remediation_df
    )