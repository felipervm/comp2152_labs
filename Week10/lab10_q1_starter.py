# ============================================================
#  WEEK 10 LAB — Q1: PASSWORD VAULT
#  COMP2152 — [Your Name Here]
# ============================================================

import sqlite3


DB_NAME = "vault.db"


# --- Helpers (provided) ---
def setup_database():
    """Create the vault table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT,
        username TEXT,
        password TEXT
    )""")
    conn.commit()
    conn.close()


def display_credentials(credentials):
    """Pretty-print a list of credential rows."""
    if not credentials:
        print("  (no results)")
        return
    for row in credentials:
        print(f"  {row[1]:<14} | {row[2]:<12} | {row[3]}")


def add_credential(website, username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
        (website, username, password)
    )
    conn.commit()
    conn.close()


def get_all_credentials():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vault ORDER BY website ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def find_credential(website):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vault WHERE website = ?", (website,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  PASSWORD VAULT")
    print("=" * 60)

    setup_database()

    print("\n--- Adding Credentials ---")
    credentials = [
        ("github.com",  "admin",        "s3cur3P@ss"),
        ("google.com",  "maziar@gmail",  "MyP@ssw0rd"),
        ("netflix.com", "maziar",        "N3tfl1x!"),
        ("github.com",  "work_user",    "W0rkP@ss!"),
    ]
    for site, user, pw in credentials:
        add_credential(site, user, pw)
        print(f"  Saved: {site}" + (f" ({user.split('_')[0]})" if "_" in user else ""))

    print("\n--- All Credentials ---")
    display_credentials(get_all_credentials())

    print("\n--- Search for 'github.com' ---")
    display_credentials(find_credential("github.com"))

    print("\n--- Search for 'spotify.com' ---")
    display_credentials(find_credential("spotify.com"))

    print("\n" + "=" * 60)
