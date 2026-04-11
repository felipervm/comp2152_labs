# ============================================================
#  WEEK 13 LAB — Q2: ASCII DASHBOARD
#  COMP2152 — Felipe da Rocha Vieira Mattos
# ============================================================

# ============================================================
#  WEEK 13 LAB — Q2: ASCII DASHBOARD
#  COMP2152 — Felipe da Rocha Vieira Mattos
# ============================================================

import csv

SAMPLE_FILE = "scan_results.csv"


# --- Helper (provided) ---
def load_findings(filename):
    """Load CSV findings (from Q1)."""
    with open(filename, "r") as f:
        return list(csv.DictReader(f))


def bar_chart(data, title, max_width=30):
    print(title)
    max_val = max(count for _, count in data)

    for label, count in data:
        bar_length = int((count / max_val) * max_width)
        print(f"  {label:<15} {'█' * bar_length} {count}")


def severity_summary(findings):
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for f in findings:
        counts[f["severity"]] += 1

    return [
        ("HIGH", counts["HIGH"]),
        ("MEDIUM", counts["MEDIUM"]),
        ("LOW", counts["LOW"])
    ]


def timeline(findings):
    counts = {}

    for f in findings:
        date = f["date"]
        counts[date] = counts.get(date, 0) + 1

    return sorted(counts.items(), key=lambda x: x[0])


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q2: ASCII DASHBOARD")
    print("=" * 60)

    findings = load_findings(SAMPLE_FILE)

    print()
    sev = severity_summary(findings)
    if sev:
        bar_chart(sev, "SEVERITY BREAKDOWN")

    print()
    dates = timeline(findings)
    if dates:
        bar_chart(dates, "FINDINGS BY DATE")

    print()
    # Count by type for a third chart
    type_counts = {}
    for f in findings:
        t = f["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    type_data = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    if type_data:
        bar_chart(type_data, "VULNERABILITY TYPES")

    print("\n" + "=" * 60)