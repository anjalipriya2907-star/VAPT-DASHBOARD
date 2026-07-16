import pandas as pd


# ==========================================================
# Dashboard Generator
# ==========================================================

def generate_dashboard_data(tracking_df):

    tracking = tracking_df.copy()

    tracking.columns = tracking.columns.str.strip()

    # ------------------------------------------------------
    # Normalize Severity
    # ------------------------------------------------------

    tracking["Severity"] = (
        tracking["Severity"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # ------------------------------------------------------
    # Normalize Status
    # ------------------------------------------------------

    tracking["Status"] = (
        tracking["Status"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # ======================================================
    # Executive Summary
    # ======================================================

    executive_df = pd.DataFrame({

        "Metric": [
            "Critical",
            "High",
            "Medium",
            "Low",
            "Open",
            "Closed",
            "Total Findings",
            "Applications"
        ],

        "Value": [

            len(tracking[tracking["Severity"] == "Critical"]),

            len(tracking[tracking["Severity"] == "High"]),

            len(tracking[tracking["Severity"] == "Medium"]),

            len(tracking[tracking["Severity"] == "Low"]),

            len(tracking[tracking["Status"] == "Open"]),

            len(tracking[tracking["Status"] == "Closed"]),

            len(tracking),

            tracking["Application"].nunique()

        ]

    })

    # ======================================================
    # Scan History
    # ======================================================

    history_rows = []

    # -------- First Found --------

    if "First Found" in tracking.columns:

        first = tracking.copy()

        first["Scan Date"] = pd.to_datetime(
            first["First Found"],
            errors="coerce",
            dayfirst=True
        )

        first = first.dropna(subset=["Scan Date"])

        for date, grp in first.groupby("Scan Date"):

            history_rows.append({

                "Scan Date": date,

                "Critical": len(grp[grp["Severity"] == "Critical"]),

                "High": len(grp[grp["Severity"] == "High"]),

                "Medium": len(grp[grp["Severity"] == "Medium"]),

                "Low": len(grp[grp["Severity"] == "Low"]),

                "Event": "First Found"

            })

    # -------- Closed Date --------

    if "Closed Date" in tracking.columns:

        closed = tracking.copy()

        closed["Scan Date"] = pd.to_datetime(
            closed["Closed Date"],
            errors="coerce",
            dayfirst=True
        )

        closed = closed.dropna(subset=["Scan Date"])

        for date, grp in closed.groupby("Scan Date"):

            history_rows.append({

                "Scan Date": date,

                "Critical": len(grp[grp["Severity"] == "Critical"]),

                "High": len(grp[grp["Severity"] == "High"]),

                "Medium": len(grp[grp["Severity"] == "Medium"]),

                "Low": len(grp[grp["Severity"] == "Low"]),

                "Event": "Closed"

            })

    if len(history_rows) > 0:

        history_df = pd.DataFrame(history_rows)

        history_df = history_df.groupby(
            "Scan Date",
            as_index=False
        ).sum(numeric_only=True)

        history_df = history_df.sort_values(
            "Scan Date"
        )

        history_df["Scan Date"] = history_df[
            "Scan Date"
        ].dt.strftime("%d-%b-%Y")

    else:

        history_df = pd.DataFrame({

            "Scan Date": [],

            "Critical": [],

            "High": [],

            "Medium": [],

            "Low": []

        })

    # ======================================================
    # Remediation Progress
    # ======================================================

    remediation_df = (

        tracking

        .groupby("Status")

        .size()

        .reset_index(name="Count")

    )

    # ======================================================
    # Save
    # ======================================================

    return (

        executive_df,

        tracking,

        history_df,

        remediation_df

    )