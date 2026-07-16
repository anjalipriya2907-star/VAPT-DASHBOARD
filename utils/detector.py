import pandas as pd


def detect_scanner(file):

    try:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file, nrows=5)
        else:
            df = pd.read_excel(file, sheet_name="Vulnerability Tracking", nrows=5)

    except:
        return "Unknown"

    columns = [str(c).strip().lower() for c in df.columns]

    # -------- Manual Report --------

    manual_required = [
        "vulnerability id",
        "vulnerability",
        "severity",
        "application",
        "status"
    ]

    if all(col in columns for col in manual_required):
        return "Manual Report"

    # -------- Burp --------

    burp_required = [
        "issue",
        "host",
        "severity"
    ]

    if all(col in columns for col in burp_required):
        return "Burp Suite"

    # -------- ZAP --------

    zap_required = [
        "alert",
        "risk",
        "url"
    ]

    if all(col in columns for col in zap_required):
        return "OWASP ZAP"

    # -------- Nessus --------

    nessus_required = [
        "plugin id",
        "plugin name",
        "risk"
    ]

    if all(col in columns for col in nessus_required):
        return "Nessus"

    return "Unknown"