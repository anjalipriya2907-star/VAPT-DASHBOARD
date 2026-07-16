import streamlit as st
import pandas as pd
import plotly.express as px


def show_remediation(remediation_df):

    st.title("🛠 Remediation Dashboard")

    remediation = remediation_df.copy()

    remediation.columns = remediation.columns.str.strip()

    st.subheader("Remediation Progress")

    st.dataframe(
        remediation,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    if len(remediation.columns) >= 2:

        x = remediation.columns[0]
        y = remediation.columns[1]

        fig = px.bar(
            remediation,
            x=x,
            y=y,
            color=x,
            text=y,
            title="Remediation Progress"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig = px.pie(
            remediation,
            names=x,
            values=y,
            hole=0.60,
            title="Remediation Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.download_button(
        "📥 Download Remediation Report",
        remediation.to_csv(index=False),
        "remediation_report.csv",
        "text/csv"
    )