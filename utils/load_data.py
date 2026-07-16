import os
import streamlit as st
import pandas as pd


def load_excel():

    # -----------------------------------------
    # Use uploaded data if available
    # -----------------------------------------

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

    # -----------------------------------------
    # Load default Excel (only if it exists)
    # -----------------------------------------

    file = "data/VAPT_Report.xlsx"

    if os.path.exists(file):

        executive_df = pd.read_excel(
            file,
            sheet_name="Executive Summary"
        )

        tracking_df = pd.read_excel(
            file,
            sheet_name="Vulnerability Tracking"
        )

        history_df = pd.read_excel(
            file,
            sheet_name="Scan History"
        )

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

    # -----------------------------------------
    # No default report found
    # -----------------------------------------

    st.info("📂 Please upload a VAPT report from the Report Ingestion page.")

    return None, None, None, None