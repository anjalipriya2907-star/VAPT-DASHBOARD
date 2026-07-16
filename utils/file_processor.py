import pandas as pd
from datetime import datetime


# ==========================================================
# Standard Columns
# ==========================================================

STANDARD_COLUMNS = [
    "Vulnerability ID",
    "Vulnerability",
    "CVE",
    "Application",
    "Testing Type",
    "Source",
    "Severity",
    "First Found",
    "Last Checked",
    "Status",
    "Closed Date",
    "Scanner"
]


# ==========================================================
# Severity Normalization
# ==========================================================

SEVERITY_MAP = {
    "critical": "Critical",
    "crititical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "info": "Low",
    "informational": "Low"
}


# ==========================================================
# Helper
# ==========================================================

def normalize_severity(value):

    value = str(value).strip().lower()

    return SEVERITY_MAP.get(value, str(value).title())


# ==========================================================
# Create Empty Standard DF
# ==========================================================

def create_standard_df(rows):

    df = pd.DataFrame(columns=STANDARD_COLUMNS)

    if rows > 0:

        df = pd.DataFrame(index=range(rows))

        for col in STANDARD_COLUMNS:

            df[col] = ""

    return df


# ==========================================================
# Main Processor
# ==========================================================

def process_file(file, scanner):

    # ------------------------------------------------------
    # Read File
    # ------------------------------------------------------

    if file.name.endswith(".csv"):

        raw = pd.read_csv(file)

    else:

        raw = pd.read_excel(
            file,
            sheet_name="Vulnerability Tracking"
        )

    raw.columns = raw.columns.str.strip()

    standard = create_standard_df(len(raw))

    today = datetime.today().strftime("%d-%b-%y")

    # ======================================================
    # Manual Report
    # ======================================================

    if scanner == "Manual Report":

        standard["Vulnerability ID"] = raw.get("Vulnerability ID", "")
        standard["Vulnerability"] = raw.get("Vulnerability", "")
        standard["CVE"] = raw.get("CVE", "")
        standard["Application"] = raw.get("Application", "")
        standard["Testing Type"] = raw.get("Testing Type", "Manual")
        standard["Source"] = raw.get("Source", "Manual")

        standard["Severity"] = raw["Severity"].apply(
            normalize_severity
        )

        standard["First Found"] = raw.get("First Found", today)
        standard["Last Checked"] = raw.get("Last Checked", today)

        standard["Status"] = (
            raw["Status"]
            .astype(str)
            .str.title()
        )

        standard["Closed Date"] = raw.get("Closed Date", "")

        standard["Scanner"] = "Manual"

        return standard

    # ======================================================
    # Burp Suite
    # ======================================================

    elif scanner == "Burp Suite":

        standard["Vulnerability"] = raw["Issue"]
        standard["Application"] = raw["Host"]

        standard["Severity"] = raw["Severity"].apply(
            normalize_severity
        )

        standard["Testing Type"] = "DAST"

        standard["Source"] = "Tool"

        standard["Status"] = "Open"

        standard["First Found"] = today

        standard["Last Checked"] = today

        standard["Scanner"] = "Burp Suite"

        return standard

    # ======================================================
    # OWASP ZAP
    # ======================================================

    elif scanner == "OWASP ZAP":

        standard["Vulnerability"] = raw["Alert"]

        standard["Application"] = raw["URL"]

        standard["Severity"] = raw["Risk"].apply(
            normalize_severity
        )

        standard["Testing Type"] = "DAST"

        standard["Source"] = "Tool"

        standard["Status"] = "Open"

        standard["First Found"] = today

        standard["Last Checked"] = today

        standard["Scanner"] = "OWASP ZAP"

        return standard

    # ======================================================
    # Nessus
    # ======================================================

    elif scanner == "Nessus":

        standard["Vulnerability"] = raw["Plugin Name"]

        standard["Application"] = raw["Host"]

        standard["Severity"] = raw["Risk"].apply(
            normalize_severity
        )

        standard["Testing Type"] = "Infrastructure"

        standard["Source"] = "Tool"

        standard["Status"] = "Open"

        standard["First Found"] = today

        standard["Last Checked"] = today

        standard["Scanner"] = "Nessus"

        return standard

    # ======================================================
    # Unknown
    # ======================================================

    return standard