# ============================================================
#  WEEK 12 LAB — Q2: DUNDER METHODS
#  COMP2152 — Felipe da Rocha Vieira Mattos
# ============================================================

class Finding:

    def __init__(self, subdomain, title, severity):
        self.subdomain = subdomain
        self.title = title
        self.severity = severity
        self.severity_rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

    def __str__(self):
        return f"[{self.severity}] {self.subdomain} — {self.title}"

    def __eq__(self, other):
        return (
            self.subdomain == other.subdomain and
            self.title == other.title
        )

    def __lt__(self, other):
        return self.severity_rank[self.severity] < self.severity_rank[other.severity]


class Report:

    def __init__(self, team_name):
        self.team_name = team_name
        self.findings = []

    def add(self, finding):
        self.findings.append(finding)

    def __len__(self):
        return len(self.findings)

    def __add__(self, other):
        new_report = Report(f"Merged: {self.team_name} + {other.team_name}")
        new_report.findings = self.findings + other.findings
        return new_report


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q2: DUNDER METHODS")
    print("=" * 60)

    f1 = Finding("ssh.0x10.cloud", "Default creds", "HIGH")
    f2 = Finding("blog.0x10.cloud", "No HTTPS", "LOW")
    f3 = Finding("api.0x10.cloud", "Version exposed", "MEDIUM")
    f1_copy = Finding("ssh.0x10.cloud", "Default creds", "HIGH")

    print("\n--- Findings ---")
    print(f"  {f1}")
    print(f"  {f2}")
    print(f"  {f3}")

    print("\n--- Comparing ---")
    eq1 = f1 == f1_copy
    eq2 = f1 == f2
    print(f"  f1 == f1_copy: {eq1}")
    print(f"  f1 == f2: {eq2}")

    print("\n--- Sorting (LOW → HIGH) ---")
    findings = [f1, f2, f3]
    try:
        for f in sorted(findings):
            print(f"  {f}")
    except TypeError:
        print("  (sorting not implemented yet)")

    print("\n--- Report Length ---")
    r1 = Report("Team Alpha")
    r1.add(f1)
    r1.add(f2)
    r2 = Report("Team Beta")
    r2.add(f3)

    len1 = len(r1)
    len2 = len(r2)
    print(f"  Team Alpha has {len1} findings")
    print(f"  Team Beta has {len2} findings")

    print("\n--- Merging Reports ---")
    try:
        merged = r1 + r2
        merged_len = len(merged)
        print(f"  {merged.team_name} has {merged_len} findings")
    except TypeError:
        print("  (merging not implemented yet)")

    print("\n" + "=" * 60)