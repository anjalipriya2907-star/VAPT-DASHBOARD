import pandas as pd


# ==========================================================
# Dashboard Statistics
# ==========================================================

def calculate_dashboard_stats(tracking_df):

    tracking = tracking_df.copy()

    tracking.columns = tracking.columns.str.strip()

    total = len(tracking)

    critical = len(
        tracking[
            tracking["Severity"] == "Critical"
        ]
    )

    high = len(
        tracking[
            tracking["Severity"] == "High"
        ]
    )

    medium = len(
        tracking[
            tracking["Severity"] == "Medium"
        ]
    )

    low = len(
        tracking[
            tracking["Severity"] == "Low"
        ]
    )

    open_count = len(
        tracking[
            tracking["Status"] == "Open"
        ]
    )

    closed_count = len(
        tracking[
            tracking["Status"] == "Closed"
        ]
    )

    applications = tracking["Application"].nunique()

    sources = tracking["Source"].nunique()

    scanners = sorted(
        tracking["Source"]
        .astype(str)
        .unique()
        .tolist()
    )

    severity_chart = (
        tracking.groupby("Severity")
        .size()
        .reset_index(name="Count")
    )

    status_chart = (
        tracking.groupby("Status")
        .size()
        .reset_index(name="Count")
    )

    application_chart = (
        tracking.groupby("Application")
        .size()
        .reset_index(name="Findings")
        .sort_values(
            by="Findings",
            ascending=False
        )
    )

    scanner_chart = (
        tracking.groupby("Source")
        .size()
        .reset_index(name="Findings")
    )

    return {

        "tracking": tracking,

        "total": total,

        "critical": critical,

        "high": high,

        "medium": medium,

        "low": low,

        "open": open_count,

        "closed": closed_count,

        "applications": applications,

        "sources": sources,

        "scanners": scanners,

        "severity_chart": severity_chart,

        "status_chart": status_chart,

        "application_chart": application_chart,

        "scanner_chart": scanner_chart

    }