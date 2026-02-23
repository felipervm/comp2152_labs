# ============================================================
#  WEEK 06 LAB: NETWORK DIAGNOSTIC LOGGER
#  COMP2152 — Windows Version
#  Felipe
# ============================================================

import subprocess
import csv
from datetime import datetime


# ===================================================
#  SECTION A: Running System Commands
# ============================================================

def run_ping(host):
    result = subprocess.run(
        ["ping", "-n", "3", host],
        capture_output=True, text=True
    )
    return result.stdout


def run_nslookup(domain):
    result = subprocess.run(
        ["nslookup", domain],
        capture_output=True, text=True
    )
    return result.stdout


def get_network_info():
    result = subprocess.run(
        ["ipconfig", "/all"],
        capture_output=True, text=True
    )
    return result.stdout


def get_arp_table():
    result = subprocess.run(
        ["arp", "-a"],
        capture_output=True, text=True
    )
    return result.stdout


def get_hostname():
    result = subprocess.run(
        ["hostname"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


# ============================================================
#  SECTION B: Parsing Command Output
# ============================================================

def parse_ping(output):
    lines = output.strip().split("\n")
    stats = {
        "transmitted": 0,
        "received": 0,
        "loss": "100%",
        "avg_ms": "N/A",
        "status": "Failed"
    }

    for line in lines:
        if "Sent =" in line and "Received =" in line:
            parts = line.split(",")
            for part in parts:
                part = part.strip()
                if "Sent" in part:
                    stats["transmitted"] = int(part.split("=")[1].strip())
                if "Received" in part:
                    stats["received"] = int(part.split("=")[1].strip())
                if "%" in part and "loss" in part:
                    loss_text = part.strip().strip("(").strip(")")
                    stats["loss"] = loss_text.split("%")[0].strip() + "%"

        if "Average" in line:
            avg_part = line.split("=")[-1].strip()
            stats["avg_ms"] = avg_part.replace("ms", "").strip()

    if stats["received"] > 0:
        stats["status"] = "Success"

    return stats


def parse_nslookup(output):
    lines = output.strip().split("\n")
    result = {"ip": "Not found", "status": "Failed"}

    found_answer = False
    for line in lines:
        if "Non-authoritative answer" in line:
            found_answer = True
        if found_answer and "Address:" in line:
            ip = line.split("Address:")[1].strip()
            if ip and "." in ip:
                result["ip"] = ip
                result["status"] = "Success"
                break

    return result


def parse_mac_address(output):
    lines = output.strip().split("\n")
    info = {"mac": "Not found", "ip": "Not found"}

    for line in lines:
        line = line.strip()
        if "Physical Address" in line and ":" in line:
            mac = line.split(":")[1].strip()
            if mac and info["mac"] == "Not found":
                info["mac"] = mac
        if "IPv4 Address" in line and ":" in line:
            ip = line.split(":")[-1].strip()
            ip = ip.replace("(Preferred)", "").strip()
            if ip and info["ip"] == "Not found":
                info["ip"] = ip

    return info


def parse_arp_table(output):
    lines = output.strip().split("\n")
    devices = []

    for line in lines:
        line = line.strip()
        parts = line.split()
        if len(parts) >= 3:
            ip = parts[0]
            mac = parts[1]
            if "." in ip and ("-" in mac or ":" in mac):
                if mac.lower() != "ff-ff-ff-ff-ff-ff":
                    devices.append({"ip": ip, "mac": mac})

    return devices


# ============================================================
#  SECTION C: File I/O — Text Files
# ============================================================

def write_to_log(filename, entry):
    with open(filename, "a") as file:
        file.write(entry + "\n")


def read_log(filename):
    with open(filename, "r") as file:
        return file.read()


def log_command_result(command_name, target, output, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + command_name + " " + target + "\n"
    entry += output
    entry += "-" * 40
    write_to_log(filename, entry)


# ============================================================
#  SECTION D: CSV Logging
# ============================================================

LOG_FILE = "diagnostics.csv"


def log_to_csv(filename, command, target, result, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, command, target, result, status])


def read_csv_log(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            print(" | ".join(row))


def analyze_csv_log(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) == 0:
        print("Log is empty.")
        return

    total = len(rows)
    print("Total entries: " + str(total))

    command_counts = {}
    status_counts = {}

    for row in rows:
        command = row[1]
        status = row[4]

        command_counts[command] = command_counts.get(command, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    print("\nCommands run:")
    for cmd in command_counts:
        print("  " + cmd + ": " + str(command_counts[cmd]) + " time(s)")

    print("\nResults:")
    for status in status_counts:
        print("  " + status + ": " + str(status_counts[status]))


# ============================================================
#  SECTION E: Exception Handling
# ============================================================

def safe_read_log(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            if content == "":
                print("Log file is empty.")
                return ""
            return content
    except FileNotFoundError:
        print("No log file found. Run a diagnostic first.")
        return ""
    finally:
        print("Log read attempt completed.")


def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt)
        if choice in valid_options:
            return choice
        else:
            print("Invalid input. Please enter one of: " + ", ".join(valid_options))


# ============================================================
#  SECTION F: Integrated Program
# ============================================================

def display_menu():
    print("\n" + "=" * 34)
    print("   NETWORK DIAGNOSTIC LOGGER")
    print("=" * 34)
    print("1. Ping a host")
    print("2. DNS Lookup (nslookup)")
    print("3. Show Network Info (MAC/IP)")
    print("4. Show ARP Table (local devices)")
    print("5. View full log")
    print("6. Analyze log (summary)")
    print("7. Quit")
    print("=" * 34)


def do_ping():
    host = input("Enter hostname to ping: ")
    print("Running ping on " + host + "...")

    output = safe_ping(host)
    ping_data = parse_ping(output)

    print("  Status:      " + ping_data["status"])
    print("  Packets:     " + str(ping_data["transmitted"]) + " sent, " + str(ping_data["received"]) + " received")
    print("  Packet Loss: " + ping_data["loss"])
    print("  Avg Latency: " + str(ping_data["avg_ms"]) + " ms")

    log_to_csv(LOG_FILE, "ping", host, ping_data["avg_ms"], ping_data["status"])
    log_command_result("PING", host, output, "network_log.txt")
    print("Result logged.")


def do_nslookup():
    domain = input("Enter domain to lookup: ")
    print("Running nslookup on " + domain + "...")

    dns_data = safe_nslookup(domain)

    print("  Status:  " + dns_data["status"])
    print("  Domain:  " + domain)
    print("  IP:      " + dns_data["ip"])

    log_to_csv(LOG_FILE, "nslookup", domain, dns_data["ip"], dns_data["status"])
    print("Result logged.")


def do_network_info():
    print("Fetching network info...")
    hostname = get_hostname()

    try:
        output = get_network_info()
        net_data = parse_mac_address(output)

        print("  Hostname:    " + hostname)
        print("  MAC Address: " + net_data["mac"])
        print("  IP Address:  " + net_data["ip"])

        log_to_csv(LOG_FILE, "ipconfig", "all", net_data["mac"] + " / " + net_data["ip"], "Captured")
        print("Result logged.")
    except Exception as e:
        print("  Error: " + str(e))
        log_to_csv(LOG_FILE, "ipconfig", "all", "Error", "Failed")


def do_arp_table():
    print("Scanning local network (ARP table)...")

    try:
        output = get_arp_table()
        devices = parse_arp_table(output)

        if len(devices) == 0:
            print("  No devices found.")
        else:
            print("  Found " + str(len(devices)) + " device(s):\n")
            for device in devices:
                print("    IP: " + device["ip"] + "  |  MAC: " + device["mac"])

        log_to_csv(LOG_FILE, "arp", "local", str(len(devices)) + " devices", "Captured")
        print("\nResult logged.")
    except Exception as e:
        print("  Error: " + str(e))


def do_view_log():
    print("\n=== FULL LOG ===")
    try:
        read_csv_log(LOG_FILE)
    except FileNotFoundError:
        print("No log file found. Run a diagnostic first.")


def do_analyze():
    print("\n=== LOG ANALYSIS ===")
    try:
        analyze_csv_log(LOG_FILE)
    except FileNotFoundError:
        print("No log file found. Run some diagnostics first.")


def main():
    hostname = get_hostname()
    print("Welcome to the Network Diagnostic Logger!")
    print("Running on: " + hostname)

    while True:
        display_menu()
        choice = get_valid_input(
            "Enter your choice (1-7): ",
            ["1", "2", "3", "4", "5", "6", "7"]
        )

        if choice == "1":
            do_ping()
        elif choice == "2":
            do_nslookup()
        elif choice == "3":
            do_network_info()
        elif choice == "4":
            do_arp_table()
        elif choice == "5":
            do_view_log()
        elif choice == "6":
            do_analyze()
        elif choice == "7":
            print("Goodbye! Your log is saved in " + LOG_FILE)
            break


main()