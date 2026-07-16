import streamlit as st
import pandas as pd
import plotly.express as px


def show_scan_history(tracking_df):

    st.title("📜 Scan History")
    st.caption("Track vulnerabilities across all scans")

    if tracking_df is None or tracking_df.empty:
        st.warning("No scan history available.")
        return

    df = tracking_df.copy()

    df.columns = df.columns.str.strip()

    required = [
        "First Found",
        "Severity",
        "Vulnerability"
    ]

    for col in required:
        if col not in df.columns:
            st.error(f"Missing column: {col}")
            return

    df = df[required].copy()

    df["Severity"] = (
        df["Severity"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["First Found"] = pd.to_datetime(
        df["First Found"],
        errors="coerce"
    )

    df.dropna(inplace=True)

    # -------------------------
    # SIDEBAR FILTERS
    # -------------------------

    st.sidebar.markdown("## 🔍 Scan Filters")

    dates = sorted(
        df["First Found"].dt.strftime("%d-%b-%Y").unique()
    )

    selected_date = st.sidebar.selectbox(
        "Scan Date",
        ["All"] + dates
    )

    severity_filter = st.sidebar.multiselect(
        "Severity",
        ["Critical", "High", "Medium", "Low"],
        default=["Critical", "High", "Medium", "Low"]
    )

    search = st.sidebar.text_input(
        "Search Vulnerability"
    )

    # -------------------------
    # APPLY FILTERS
    # -------------------------

    filtered = df.copy()

    if selected_date != "All":
        filtered = filtered[
            filtered["First Found"].dt.strftime("%d-%b-%Y")
            == selected_date
        ]

    filtered = filtered[
        filtered["Severity"].isin(severity_filter)
    ]

    if search:

        filtered = filtered[
            filtered["Vulnerability"]
            .str.contains(search,
                          case=False,
                          na=False)
        ]

    # -------------------------
    # KPI CARDS
    # -------------------------

    total_scans = (
        filtered["First Found"]
        .dt.strftime("%d-%b-%Y")
        .nunique()
    )

    critical = len(
        filtered[
            filtered["Severity"]=="Critical"
        ]
    )

    high = len(
        filtered[
            filtered["Severity"]=="High"
        ]
    )

    medium = len(
        filtered[
            filtered["Severity"]=="Medium"
        ]
    )

    low = len(
        filtered[
            filtered["Severity"]=="Low"
        ]
    )

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric("Total Scans", total_scans)
    c2.metric("Critical", critical)
    c3.metric("High", high)
    c4.metric("Medium", medium)
    c5.metric("Low", low)

        # =========================================================
    # SEVERITY DISTRIBUTION
    # =========================================================

    st.markdown("---")
    st.subheader("📊 Severity Distribution")

    severity_counts = (
        filtered["Severity"]
        .value_counts()
        .reindex(
            ["Critical", "High", "Medium", "Low"],
            fill_value=0
        )
        .reset_index()
    )

    severity_counts.columns = ["Severity", "Count"]

    fig = px.bar(
        severity_counts,
        x="Severity",
        y="Count",
        color="Severity",
        text="Count",
        title="Overall Severity Distribution"
    )

    fig.update_layout(
        height=420,
        xaxis_title="Severity",
        yaxis_title="Number of Vulnerabilities"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================================================
    # SCAN SUMMARY TABLE
    # =========================================================

    st.markdown("---")
    st.subheader("📅 Scan Summary")

    summary = (
        filtered.groupby(
            [
                filtered["First Found"].dt.strftime("%d-%b-%Y"),
                "Severity"
            ]
        )
        .size()
        .unstack(fill_value=0)
    )

    for sev in ["Critical", "High", "Medium", "Low"]:
        if sev not in summary.columns:
            summary[sev] = 0

    summary = summary[
        ["Critical", "High", "Medium", "Low"]
    ]

    summary = summary.reset_index()

    summary.rename(
        columns={
            "First Found":"Scan Date"
        },
        inplace=True
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    # =========================================================
    # DOWNLOAD
    # =========================================================

    csv = summary.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Scan Summary",
        csv,
        "scan_history.csv",
        "text/csv"
    )

    st.markdown("---")

        # =========================================================
    # DETAILED SCAN HISTORY
    # =========================================================

    st.subheader("📂 Detailed Scan History")

    grouped = filtered.groupby("First Found")

    if len(grouped) == 0:
        st.info("No scan data available for the selected filters.")
        return

    for scan_date, group in grouped:

        total = len(group)

        critical = group[group["Severity"] == "Critical"]["Vulnerability"].tolist()
        high = group[group["Severity"] == "High"]["Vulnerability"].tolist()
        medium = group[group["Severity"] == "Medium"]["Vulnerability"].tolist()
        low = group[group["Severity"] == "Low"]["Vulnerability"].tolist()

        with st.expander(
            f"📅 {scan_date.strftime('%d %b %Y')}  |  Total Findings : {total}",
            expanded=False
        ):

            # Summary Metrics
            m1, m2, m3, m4 = st.columns(4)

            m1.metric("🔴 Critical", len(critical))
            m2.metric("🟠 High", len(high))
            m3.metric("🟡 Medium", len(medium))
            m4.metric("🟢 Low", len(low))

            st.markdown("---")

            left, right = st.columns(2)

            with left:

                st.markdown("### 🔴 Critical")

                if critical:
                    for item in critical:
                        st.error(item)
                else:
                    st.success("No Critical Vulnerabilities")

                st.markdown("### 🟠 High")

                if high:
                    for item in high:
                        st.warning(item)
                else:
                    st.success("No High Vulnerabilities")

            with right:

                st.markdown("### 🟡 Medium")

                if medium:
                    for item in medium:
                        st.info(item)
                else:
                    st.success("No Medium Vulnerabilities")

                st.markdown("### 🟢 Low")

                if low:
                    for item in low:
                        st.write("🟢", item)
                else:
                    st.success("No Low Vulnerabilities")

            # Detailed Table
            st.markdown("---")
            st.markdown("#### 📋 Complete Findings")

            display = group.copy()

            display = display.sort_values(
                by="Severity"
            )

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")
    st.success("✅ Scan History Loaded Successfully")