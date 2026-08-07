#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "[+] Checking Python..."
pkg install -y python

echo "[+] Starting Local OTP Lab..."
python otp_lab.py
