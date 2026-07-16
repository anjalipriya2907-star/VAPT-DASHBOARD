import streamlit as st
import pandas as pd
from io import BytesIO


def show_reports(executive_df,
                 tracking_df,
                 history_df,
                 remediation_df):

    st.title("📄 Reports Center")

    st.write("Download reports in CSV or Excel format.")

    st.divider()

    # ------------------------------------
    # CSV Downloads
    # ------------------------------------

    st.subheader("CSV Reports")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(

            "📥 Executive Summary",

            executive_df.to_csv(index=False),

            "Executive_Summary.csv",

            "text/csv"

        )

        st.download_button(

            "📥 Vulnerability Tracking",

            tracking_df.to_csv(index=False),

            "Vulnerability_Tracking.csv",

            "text/csv"

        )

    with col2:

        st.download_button(

            "📥 Scan History",

            history_df.to_csv(index=False),

            "Scan_History.csv",

            "text/csv"

        )

        st.download_button(

            "📥 Remediation Progress",

            remediation_df.to_csv(index=False),

            "Remediation_Progress.csv",

            "text/csv"

        )

    st.divider()

    # ------------------------------------
    # Combined Excel Report
    # ------------------------------------

    st.subheader("Combined Excel Report")

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        executive_df.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False
        )

        tracking_df.to_excel(
            writer,
            sheet_name="Vulnerability Tracking",
            index=False
        )

        history_df.to_excel(
            writer,
            sheet_name="Scan History",
            index=False
        )

        remediation_df.to_excel(
            writer,
            sheet_name="Remediation Progress",
            index=False
        )

    st.download_button(

        "📥 Download Complete Excel Report",

        output.getvalue(),

        "VAPT_Report.xlsx",

        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    st.divider()

    # ------------------------------------
    # Summary
    # ------------------------------------

    st.subheader("Project Summary")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Executive Records",
            len(executive_df)
        )

        st.metric(
            "Tracked Vulnerabilities",
            len(tracking_df)
        )

    with c2:

        st.metric(
            "Scan History Records",
            len(history_df)
        )

        st.metric(
            "Remediation Records",
            len(remediation_df)
        )

    st.success("Reports generated successfully.")