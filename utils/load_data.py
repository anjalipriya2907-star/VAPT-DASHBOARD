import streamlit as st
import pandas as pd


def load_excel():

    # -------------------------------------------------
    # Use uploaded data if available
    # -------------------------------------------------

    if (
        "tracking_df" in st.session_state
        and "executive_df" in st.session_state
        and "history_df" in st.session_state
        and "remediation_df" in st.session_state
    ):

        return (
            st.session_state["executive_df"],
            st.session_state["tracking_df"],
            st.session_state["history_df"],
            st.session_state["remediation_df"]
        )

    # -------------------------------------------------
    # Load default Excel file
    # -------------------------------------------------

    file = "data/VAPT_Report.xlsx"

    # Executive Summary
    executive_df = pd.read_excel(
        file,
        sheet_name="Executive Summary"
    )

    # Vulnerability Tracking
    tracking_df = pd.read_excel(
        file,
        sheet_name="Vulnerability Tracking"
    )

    # Scan History
    history_df = pd.read_excel(
        file,
        sheet_name="Scan History"
    )

    # Remediation Progress
    remediation_df = pd.read_excel(
        file,
        sheet_name="Remediation Progress"
    )

    return (
        executive_df,
        tracking_df,
        history_df,
        remediation_df
    )