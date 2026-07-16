import streamlit as st
import plotly.express as px

from utils.dashboard_stats import calculate_dashboard_stats


def show_dashboard(executive_df, tracking_df, history_df, remediation_df):

    stats = calculate_dashboard_stats(tracking_df)
    tracking = stats["tracking"]

    st.title("🛡 Unified Vulnerability Management Dashboard")

    st.divider()

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    row1 = st.columns(4)

    row1[0].metric("🔴 Critical", stats["critical"])
    row1[1].metric("🟠 High", stats["high"])
    row1[2].metric("🟡 Medium", stats["medium"])
    row1[3].metric("🟢 Low", stats["low"])

    row2 = st.columns(4)

    row2[0].metric("📋 Total Findings", stats["total"])
    row2[1].metric("🔓 Open", stats["open"])
    row2[2].metric("✅ Closed", stats["closed"])
    row2[3].metric("💻 Applications", stats["applications"])

    st.divider()

    # ==========================================================
    # CHARTS
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:

        severity_fig = px.pie(
            stats["severity_chart"],
            names="Severity",
            values="Count",
            hole=0.60,
            title="Severity Distribution"
        )

        st.plotly_chart(
            severity_fig,
            use_container_width=True,
            key="dashboard_severity"
        )

    with col2:

        status_fig = px.bar(
            stats["status_chart"],
            x="Status",
            y="Count",
            color="Status",
            text="Count",
            title="Status Distribution"
        )

        st.plotly_chart(
            status_fig,
            use_container_width=True,
            key="dashboard_status"
        )

    st.divider()

    # ==========================================================
    # APPLICATIONS
    # ==========================================================

    application_fig = px.bar(
        stats["application_chart"],
        x="Application",
        y="Findings",
        color="Application",
        text="Findings",
        title="Top Affected Applications"
    )

    st.plotly_chart(
        application_fig,
        use_container_width=True,
        key="dashboard_application"
    )

    st.divider()

    # ==========================================================
    # SOURCE DISTRIBUTION
    # ==========================================================

    scanner_fig = px.pie(
        stats["scanner_chart"],
        names="Source",
        values="Findings",
        hole=0.55,
        title="Scanner Distribution"
    )

    st.plotly_chart(
        scanner_fig,
        use_container_width=True,
        key="dashboard_scanner"
    )

    st.divider()

    # ==========================================================
    # SUMMARY
    # ==========================================================

    c1, c2, c3 = st.columns(3)

    c1.metric("Applications", stats["applications"])
    c2.metric("Sources", stats["sources"])
    c3.metric("Scanners", len(stats["scanners"]))

    st.divider()

    # ==========================================================
    # RECENT FINDINGS
    # ==========================================================

    st.subheader("Recent Vulnerabilities")

    st.dataframe(
        tracking,
        use_container_width=True,
        hide_index=True
    )