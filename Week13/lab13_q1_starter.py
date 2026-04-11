# ============================================================
#  WEEK 13 LAB — Q1: SCAN DATA ANALYSIS
#  COMP2152 — Felipe da Rocha Vieira Mattos
# ============================================================

# ============================================================
#  WEEK 13 LAB — Q1: SCAN DATA ANALYSIS
#  COMP2152 — Felipe da Rocha Vieira Mattos
# ============================================================

import csv
import os

SAMPLE_FILE = "scan_results.csv"


def create_sample_data():
    data = [
        {"subdomain": "ssh.0x10.cloud",   "type": "default_creds",  "severity": "HIGH",   "date": "2026-03-10"},
        {"subdomain": "blog.0x10.cloud",  "type": "no_https",       "severity": "LOW",    "date": "2026-03-10"},
        {"subdomain": "api.0x10.cloud",   "type": "missing_header", "severity": "LOW",    "date": "2026-03-10"},
        {"subdomain": "ftp.0x10.cloud",   "type": "default_creds",  "severity": "HIGH",   "date": "2026-03-10"},
        {"subdomain": "cdn.0x10.cloud",   "type": "missing_header", "severity": "LOW",    "date": "2026-03-10"},
        {"subdomain": "db.0x10.cloud",    "type": "open_port",      "severity": "HIGH",   "date": "2026-03-11"},
        {"subdomain": "api.0x10.cloud",   "type": "open_port",      "severity": "MEDIUM", "date": "2026-03-11"},
        {"subdomain": "blog.0x10.cloud",  "type": "exposed_file",   "severity": "MEDIUM", "date": "2026-03-11"},
        {"subdomain": "admin.0x10.cloud", "type": "exposed_file",   "severity": "HIGH",   "date": "2026-03-12"},
        {"subdomain": "ssh.0x10.cloud",   "type": "open_port",      "severity": "MEDIUM", "date": "2026-03-12"},
        {"subdomain": "dev.0x10.cloud",   "type": "missing_header", "severity": "LOW",    "date": "2026-03-12"},
        {"subdomain": "login.0x10.cloud", "type": "default_creds",  "severity": "LOW",    "date": "2026-03-12"},
    ]
    with open(SAMPLE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["subdomain", "type", "severity", "date"])
        writer.writeheader()
        writer.writerows(data)


def load_findings(filename):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def count_by_field(findings, field):
    counts = {}
    for f in findings:
        val = f[field]
        counts[val] = counts.get(val, 0) + 1
    return counts


def filter_findings(findings, field, value):
    return [f for f in findings if f[field] == value]


def top_subdomains(findings, n):
    counts = count_by_field(findings, "subdomain")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts[:n]


if __name__ == "__main__":
    print("=" * 60)
    print("  Q1: SCAN DATA ANALYSIS")
    print("=" * 60)

    create_sample_data()
    findings = load_findings(SAMPLE_FILE)

    if findings:
        print(f"\n--- Loaded {len(findings)} findings ---")

        print("\n--- By Severity ---")
        sev = count_by_field(findings, "severity")
        for s in ["HIGH", "MEDIUM", "LOW"]:
            print(f"  {s:<8} : {sev.get(s, 0)}")

        print("\n--- By Type ---")
        types = count_by_field(findings, "type")
        for t, c in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {t:<15} : {c}")

        print("\n--- HIGH Severity Findings ---")
        highs = filter_findings(findings, "severity", "HIGH")
        for f in highs:
            print(f"  {f['subdomain']:<18} | {f['type']:<14} | {f['severity']}")

        print("\n--- Top 3 Subdomains ---")
        top = top_subdomains(findings, 3)
        for i, (sub, count) in enumerate(top, 1):
            print(f"  {i}. {sub:<20} ({count})")

    print("\n" + "=" * 60)