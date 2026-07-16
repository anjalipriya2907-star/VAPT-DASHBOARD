import streamlit as st
import pandas as pd

from utils.detector import detect_scanner
from utils.file_processor import process_file
from utils.correlator import correlate_reports
from utils.dashboard_generator import generate_dashboard_data


def show_upload_center():

    st.title("📂 Report Ingestion Center")

    st.markdown("""
Upload multiple vulnerability reports.

### Supported Formats
- Excel (.xlsx)
- CSV (.csv)


""")

    uploaded_files = st.file_uploader(
        "Upload Reports",
        type=["xlsx", "csv"],
        accept_multiple_files=True
    )

    if not uploaded_files:
        st.info("Upload one or more reports.")
        return

    st.success(f"{len(uploaded_files)} file(s) uploaded.")

    summary = []
    processed_reports = []
    total_findings = 0

    for file in uploaded_files:

        scanner = detect_scanner(file)

        st.write(f"📄 {file.name} → {scanner}")

        processed = process_file(file, scanner)

        total_findings += len(processed)

        processed_reports.append(processed)

        summary.append({
            "File Name": file.name,
            "Scanner": scanner,
            "Findings": len(processed),
            "Status": "Loaded"
        })

    st.subheader("Uploaded Reports")

    st.dataframe(
        pd.DataFrame(summary),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    if st.button(
        "🚀 Process Reports",
        use_container_width=True
    ):

        with st.spinner("Processing reports..."):

            correlated = correlate_reports(
                processed_reports
            )
            st.subheader("DEBUG")

            st.write(correlated.columns.tolist())

            st.dataframe(correlated)

            executive_df, tracking_df, history_df, remediation_df = generate_dashboard_data(
                correlated
            )

            st.session_state["executive_df"] = executive_df
            st.session_state["tracking_df"] = tracking_df
            st.session_state["history_df"] = history_df
            st.session_state["remediation_df"] = remediation_df

        duplicates = total_findings - len(correlated)

        st.success("✅ Processing Completed Successfully!")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Reports",
            len(uploaded_files)
        )

        c2.metric(
            "Raw Findings",
            total_findings
        )

        c3.metric(
            "Correlated Findings",
            len(correlated)
        )

        c4.metric(
            "Duplicates Removed",
            duplicates
        )

        st.divider()

        st.subheader("Unified Vulnerability Report")

        st.dataframe(
            correlated,
            use_container_width=True,
            hide_index=True
        )

        csv = correlated.to_csv(index=False)

        st.download_button(
            "📥 Download Unified Report",
            csv,
            file_name="Unified_Report.csv",
            mime="text/csv"
        )

        st.success("Dashboard data has been updated.")