#!/usr/bin/env python3
"""
LOCAL OTP LAB v2
Local-only OTP authentication simulator.

This program does NOT send SMS, WhatsApp, email, or external API requests.
It is intended for learning and authorized testing of authentication flows.
"""

import json
import os
import secrets
import time
from datetime import datetime

VERSION = "2.0"
OTP_LENGTH = 6
OTP_EXPIRY = 60
MAX_ATTEMPTS = 3
COOLDOWN = 10
LOG_FILE = "otp_test.log"

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

otp = None
created_at = 0.0
attempts = 0
last_request = 0.0


def clear():
    os.system("clear")


def log(event, details=""):
    record = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "details": details
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def banner():
    clear()
    print(f"{GREEN}{BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║                    LOCAL OTP LAB                             ║")
    print("║             AUTHENTICATION SECURITY TOOL                     ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{RESET}{GRAY}v{VERSION} • LOCAL ONLY • TERMUX READY{RESET}\n")


def generate():
    global otp, created_at, attempts, last_request

    now = time.time()

    if last_request and now - last_request < COOLDOWN:
        wait = COOLDOWN - (now - last_request)
        print(f"\n{YELLOW}[!] Cooldown aktif. Tunggu {int(wait) + 1} detik.{RESET}")
        return

    otp = "".join(str(secrets.randbelow(10)) for _ in range(OTP_LENGTH))
    created_at = now
    last_request = now
    attempts = 0

    print(f"\n{GREEN}{BOLD}╭─ OTP GENERATED ─────────────────────────────╮{RESET}")
    print(f"{GREEN}│{RESET} Code       : {WHITE}{BOLD}{otp}{RESET}")
    print(f"{GREEN}│{RESET} Expires in : {OTP_EXPIRY} seconds")
    print(f"{GREEN}│{RESET} Attempts   : {MAX_ATTEMPTS}")
    print(f"{GREEN}╰─────────────────────────────────────────────╯{RESET}")

    log("OTP_GENERATED", "Local OTP generated")


def verify():
    global otp, attempts

    if otp is None:
        print(f"\n{YELLOW}[!] Generate an OTP first.{RESET}")
        return

    age = time.time() - created_at

    if age >= OTP_EXPIRY:
        print(f"\n{RED}[!] OTP EXPIRED{RESET}")
        log("OTP_EXPIRED", "OTP expired before verification")
        otp = None
        return

    if attempts >= MAX_ATTEMPTS:
        print(f"\n{RED}[!] VERIFICATION LOCKED{RESET}")
        log("OTP_BLOCKED", "Maximum attempts reached")
        return

    value = input(f"\n{CYAN}otp@lab:~$ {RESET}").strip()
    attempts += 1

    if secrets.compare_digest(value, otp):
        print(f"\n{GREEN}{BOLD}[✓] OTP VALID{RESET}")
        print(f"{GREEN}[+] Authentication successful.{RESET}")
        log("OTP_VERIFIED", "Successful verification")
        otp = None
        attempts = 0
    else:
        remaining = MAX_ATTEMPTS - attempts
        print(f"\n{RED}[✗] OTP INVALID{RESET}")
        print(f"{YELLOW}[!] Remaining attempts: {remaining}{RESET}")
        log("OTP_FAILED", f"Attempt {attempts}/{MAX_ATTEMPTS}")


def status():
    print(f"\n{CYAN}{BOLD}╭─ SYSTEM STATUS ─────────────────────────────╮{RESET}")

    if otp is None:
        print(f"{CYAN}│{RESET} OTP status : {GRAY}INACTIVE{RESET}")
    else:
        remaining = max(0, OTP_EXPIRY - int(time.time() - created_at))
        state = "ACTIVE" if remaining > 0 else "EXPIRED"
        color = GREEN if state == "ACTIVE" else RED
        print(f"{CYAN}│{RESET} OTP status : {color}{state}{RESET}")
        print(f"{CYAN}│{RESET} Remaining  : {remaining} seconds")
        print(f"{CYAN}│{RESET} Attempts   : {attempts}/{MAX_ATTEMPTS}")

    print(f"{CYAN}╰─────────────────────────────────────────────╯{RESET}")


def logs():
    print(f"\n{CYAN}{BOLD}╭─ SECURITY LOG ──────────────────────────────╮{RESET}")

    if not os.path.exists(LOG_FILE):
        print(f"{CYAN}│{RESET} No logs yet.")
    else:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            entries = f.readlines()[-10:]

        for line in entries:
            try:
                item = json.loads(line)
                print(
                    f"{CYAN}│{RESET} {item['time']} "
                    f"{WHITE}{item['event']}{RESET} "
                    f"{GRAY}{item['details']}{RESET}"
                )
            except (json.JSONDecodeError, KeyError):
                pass

    print(f"{CYAN}╰─────────────────────────────────────────────╯{RESET}")


def pause():
    input(f"\n{GRAY}Press Enter to continue...{RESET}")


def main():
    while True:
        banner()

        print(f"{WHITE}{BOLD}┌─ COMMAND CENTER ────────────────────────────┐{RESET}")
        print("│  [1] Generate OTP                           │")
        print("│  [2] Verify OTP                             │")
        print("│  [3] OTP Status                             │")
        print("│  [4] Security Logs                          │")
        print("│  [5] Exit                                   │")
        print(f"{WHITE}└─────────────────────────────────────────────┘{RESET}")

        choice = input(f"\n{GREEN}root@otp-lab:~$ {RESET}").strip()

        if choice == "1":
            generate()
            pause()
        elif choice == "2":
            verify()
            pause()
        elif choice == "3":
            status()
            pause()
        elif choice == "4":
            logs()
            pause()
        elif choice == "5":
            print(f"\n{GREEN}[+] Session closed.{RESET}")
            break
        else:
            print(f"\n{YELLOW}[!] Invalid option.{RESET}")
            time.sleep(0.8)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GRAY}Session interrupted.{RESET}")
