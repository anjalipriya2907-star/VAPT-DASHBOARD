import pandas as pd


# ==========================================================
# Severity Ranking
# ==========================================================

severity_rank = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}


# ==========================================================
# Correlation Engine
# ==========================================================

def correlate_reports(dataframes):

    if len(dataframes) == 0:
        return pd.DataFrame()

    merged = pd.concat(
        dataframes,
        ignore_index=True
    )

    merged.fillna("", inplace=True)

    merged.columns = merged.columns.str.strip()

    correlated = []

    grouped = merged.groupby(
        "Vulnerability",
        dropna=False
    )

    counter = 1

    for vuln, group in grouped:

        row = {}

        # -------------------------------------------------
        # Vulnerability ID
        # -------------------------------------------------

        existing_ids = group["Vulnerability ID"]

        existing_ids = existing_ids[
            existing_ids.astype(str).str.strip() != ""
        ]

        if len(existing_ids) > 0:

            row["Vulnerability ID"] = existing_ids.iloc[0]

        else:

            row["Vulnerability ID"] = f"VULN-{counter:03d}"

        counter += 1

        # -------------------------------------------------
        # Basic Information
        # -------------------------------------------------

        row["Vulnerability"] = vuln

        row["CVE"] = ", ".join(
            sorted(
                set(
                    group["CVE"]
                    .astype(str)
                    .replace("", pd.NA)
                    .dropna()
                )
            )
        )

        row["Application"] = ", ".join(
            sorted(
                set(
                    group["Application"]
                    .astype(str)
                    .replace("", pd.NA)
                    .dropna()
                )
            )
        )

        row["Testing Type"] = ", ".join(
            sorted(
                set(
                    group["Testing Type"]
                    .astype(str)
                    .replace("", pd.NA)
                    .dropna()
                )
            )
        )

        row["Source"] = ", ".join(
            sorted(
                set(
                    group["Source"]
                    .astype(str)
                    .replace("", pd.NA)
                    .dropna()
                )
            )
        )

        row["Scanner"] = ", ".join(
            sorted(
                set(
                    group["Scanner"]
                    .astype(str)
                    .replace("", pd.NA)
                    .dropna()
                )
            )
        )

        # -------------------------------------------------
        # Severity
        # -------------------------------------------------

        severities = group["Severity"].tolist()

        highest = max(
            severities,
            key=lambda x: severity_rank.get(x, 0)
        )

        row["Severity"] = highest

        # -------------------------------------------------
        # Dates
        # -------------------------------------------------

        first_found = pd.to_datetime(
            group["First Found"],
            errors="coerce"
        )

        if first_found.notna().any():

            row["First Found"] = first_found.min().strftime("%d-%b-%y")

        else:

            row["First Found"] = ""

        last_checked = pd.to_datetime(
            group["Last Checked"],
            errors="coerce"
        )

        if last_checked.notna().any():

            row["Last Checked"] = last_checked.max().strftime("%d-%b-%y")

        else:

            row["Last Checked"] = ""

        closed = pd.to_datetime(
            group["Closed Date"],
            errors="coerce"
        )

        if closed.notna().any():

            row["Closed Date"] = closed.max().strftime("%d-%b-%y")

        else:

            row["Closed Date"] = ""

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        statuses = (
            group["Status"]
            .astype(str)
            .str.title()
            .tolist()
        )

        if "Open" in statuses:

            row["Status"] = "Open"

        else:

            row["Status"] = "Closed"

        # -------------------------------------------------
        # Occurrences
        # -------------------------------------------------

        row["Occurrences"] = len(group)

        correlated.append(row)

    correlated = pd.DataFrame(correlated)

    correlated = correlated.sort_values(
        by="Severity",
        key=lambda s: s.map(severity_rank),
        ascending=False
    )

    correlated.reset_index(
        drop=True,
        inplace=True
    )

    return correlated