import streamlit as st
import pandas as pd
import plotly.express as px


def show_vulnerabilities(tracking_df):

    st.title("🐞 Vulnerability Management")

    tracking = tracking_df.copy()
    tracking.columns = tracking.columns.str.strip()

    # --------------------------------------------------
    # SEARCH & FILTERS
    # --------------------------------------------------

    st.subheader("Search & Filters")

    c1, c2 = st.columns(2)

    search = c1.text_input("🔍 Search Vulnerability / CVE")

    severity = c2.selectbox(
        "Severity",
        ["All"] + sorted(tracking["Severity"].dropna().unique().tolist())
    )

    c3, c4 = st.columns(2)

    status = c3.selectbox(
        "Status",
        ["All"] + sorted(tracking["Status"].dropna().unique().tolist())
    )

    application = c4.selectbox(
        "Application",
        ["All"] + sorted(tracking["Application"].dropna().unique().tolist())
    )

    filtered = tracking.copy()

    if search:
        filtered = filtered[
            filtered.astype(str)
            .apply(lambda x: x.str.contains(search, case=False, na=False))
            .any(axis=1)
        ]

    if severity != "All":
        filtered = filtered[filtered["Severity"] == severity]

    if status != "All":
        filtered = filtered[filtered["Status"] == status]

    if application != "All":
        filtered = filtered[filtered["Application"] == application]

    st.divider()

    # --------------------------------------------------
    # KPI
    # --------------------------------------------------

    row1 = st.columns(4)

    row1[0].metric("🔴 Critical", len(filtered[filtered["Severity"] == "Critical"]))
    row1[1].metric("🟠 High", len(filtered[filtered["Severity"] == "High"]))
    row1[2].metric("🟡 Medium", len(filtered[filtered["Severity"] == "Medium"]))
    row1[3].metric("🟢 Low", len(filtered[filtered["Severity"] == "Low"]))

    row2 = st.columns(3)

    row2[0].metric("📋 Total", len(filtered))
    row2[1].metric("🔓 Open", len(filtered[filtered["Status"] == "Open"]))
    row2[2].metric("✅ Closed", len(filtered[filtered["Status"] == "Closed"]))

    st.divider()

    # --------------------------------------------------
    # TABLE
    # --------------------------------------------------

    st.subheader("Tracked Vulnerabilities")

    st.data_editor(
        filtered,
        hide_index=True,
        use_container_width=True,
        disabled=True
    )

    st.divider()

    # --------------------------------------------------
    # DETAILS
    # --------------------------------------------------

    st.subheader("📄 Vulnerability Details")

    if len(filtered):

        if "Vulnerability" in filtered.columns:

            selected = st.selectbox(
                "Select Vulnerability",
                filtered["Vulnerability"]
            )

            details = filtered[
                filtered["Vulnerability"] == selected
            ].iloc[0]

        else:

            selected = st.selectbox(
                "Select Row",
                filtered.index
            )

            details = filtered.loc[selected]

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Basic Information")

            for column in [
                "Vulnerability",
                "CVE",
                "Application"
            ]:
                if column in details.index:
                    st.write(f"**{column}:** {details[column]}")

        with col2:

            st.write("### Scan Information")

            for column in [
                "Testing Type",
                "Source",
                "Severity",
                "Status"
            ]:
                if column in details.index:
                    st.write(f"**{column}:** {details[column]}")

        st.write("### Timeline")

        for column in [
            "First Found",
            "Last Checked",
            "Closed Date"
        ]:
            if column in details.index:
                st.write(f"**{column}:** {details[column]}")

    else:

        st.warning("No vulnerabilities found.")

    st.divider()

    # --------------------------------------------------
    # CHARTS
    # --------------------------------------------------

    left, right = st.columns(2)

    severity_chart = (
        filtered["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_chart.columns = ["Severity", "Count"]

    with left:

        fig = px.pie(
            severity_chart,
            names="Severity",
            values="Count",
            hole=0.60,
            title="Severity Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    status_chart = (
        filtered["Status"]
        .value_counts()
        .reset_index()
    )

    status_chart.columns = ["Status", "Count"]

    with right:

        fig = px.bar(
            status_chart,
            x="Status",
            y="Count",
            color="Status",
            text="Count",
            title="Open vs Closed"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # APPLICATIONS
    # --------------------------------------------------

    st.subheader("📊 Most Affected Applications")

    app_chart = (
        filtered.groupby("Application")
        .size()
        .reset_index(name="Findings")
        .sort_values(by="Findings", ascending=False)
    )

    fig = px.bar(
        app_chart,
        x="Application",
        y="Findings",
        color="Application",
        text="Findings"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------

    st.download_button(
        "📥 Download Filtered Report",
        filtered.to_csv(index=False),
        file_name="filtered_vulnerabilities.csv",
        mime="text/csv"
    )