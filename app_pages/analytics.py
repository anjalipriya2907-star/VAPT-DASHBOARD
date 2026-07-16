import streamlit as st
import pandas as pd
import plotly.express as px


def show_analytics(executive_df, tracking_df):

    st.title("📊 Security Analytics")

    tracking = tracking_df.copy()

    tracking.columns = tracking.columns.str.strip()

    # ----------------------------
    # Severity Count
    # ----------------------------

    severity = tracking.groupby(
        "Severity"
    ).size().reset_index(name="Count")

    left, right = st.columns(2)

    with left:

        fig = px.pie(

            severity,

            names="Severity",

            values="Count",

            hole=.60,

            title="Severity Distribution"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        fig = px.bar(

            severity,

            x="Severity",

            y="Count",

            color="Severity",

            text="Count",

            title="Severity Comparison"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # ----------------------------
    # Status
    # ----------------------------

    status = tracking.groupby(
        "Status"
    ).size().reset_index(name="Count")

    left,right = st.columns(2)

    with left:

        fig = px.pie(

            status,

            names="Status",

            values="Count",

            hole=.60,

            title="Open vs Closed"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        fig = px.bar(

            status,

            x="Status",

            y="Count",

            color="Status",

            text="Count",

            title="Status Comparison"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # ----------------------------
    # Application Wise
    # ----------------------------

    app = tracking.groupby(

        "Application"

    ).size().reset_index(name="Findings")

    fig = px.bar(

        app,

        x="Application",

        y="Findings",

        color="Application",

        text="Findings",

        title="Application Wise Vulnerabilities"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    st.subheader("Analytics Data")

    st.dataframe(

        tracking,

        use_container_width=True,

        hide_index=True

    )