#!/usr/bin/env python3
"""
VULNERABLE BANKING DEMO - EDUCATIONAL PURPOSES ONLY
NexusBank - Fake online banking platform full of security flaws.
"""

import os
import sqlite3
import hashlib
import jwt
import random
import subprocess
import pickle
import logging
from datetime import datetime, timedelta
from getpass import getpass

# ============================
# SECRETS & WEAK CONFIG
# ============================
JWT_SECRET = "supersecretjwtkey1234567890"   # weak & hardcoded
ADMIN_PASS = "BankMaster2026!"
DEBUG = True
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"      # fake but detectable

logging.basicConfig(level=logging.DEBUG, filename="bank.log")

# ============================
# DATABASE
# ============================
def init_bank_db():
    conn = sqlite3.connect("nexusbank.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, balance REAL, role TEXT)")
    c.execute("INSERT OR IGNORE INTO accounts VALUES (1, 'admin', 999999.0, 'admin')")
    conn.commit()
    conn.close()

# ============================
# AUTH + MULTIPLE INJECTIONS
# ============================
def authenticate(username: str, password: str):
    conn = sqlite3.connect("nexusbank.db")
    c = conn.cursor()
    # Classic SQLi
    query = f"SELECT role, balance FROM accounts WHERE username='{username}' AND password='{hashlib.sha1((password+'salt').encode()).hexdigest()}'"
    c.execute(query)
    row = c.fetchone()
    conn.close()
    return {"username": username, "role": row[0], "balance": row[1]} if row else None

# ============================
# COMMAND + FILE VULNS
# ============================
def transfer_funds(target: str, amount: str):
    # Command injection via system call
    cmd = f"echo 'Transfer {amount} to {target}' >> transactions.log"
    subprocess.run(cmd, shell=True)

def generate_report(report_type: str):
    # eval + file write
    try:
        code = f"print('Report for {report_type}: Balance = ' + str(1000))"
        exec(code)   # Dangerous
    except:
        pass

# ============================
# JWT + WEAK TOKEN
# ============================
def create_jwt(username: str):
    token = jwt.encode({"user": username, "exp": datetime.utcnow() + timedelta(days=1)}, 
                       JWT_SECRET, algorithm="HS256")
    return token

# ============================
# MAIN
# ============================
def main():
    init_bank_db()
    print("="*65)
    print("🏦 NexusBank - Secure Online Banking")
    print("="*65)
    
    session = None
    while True:
        if not session:
            print("1. Login\n2. Exit")
        else:
            print(f"Logged in: {session['username']} | Balance: ${session['balance']}")
            print("3. Transfer funds\n4. Generate report\n5. View transactions\n6. Logout")
        
        ch = input("> ").strip()

        if not session:
            if ch == "1":
                u = input("Username: ")
                p = getpass("Password: ")
                session = authenticate(u, p)
                if session:
                    print(f"[+] Logged in! JWT: {create_jwt(u)}")
            elif ch == "2":
                break
        else:
            if ch == "3":
                target = input("Target account: ")
                amt = input("Amount: ")
                transfer_funds(target, amt)
            elif ch == "4":
                rtype = input("Report type: ")
                generate_report(rtype)
            elif ch == "5":
                print("Reading transactions.log...")
                try:
                    with open("transactions.log") as f:
                        print(f.read())
                except:
                    pass
            elif ch == "6":
                session = None

if __name__ == "__main__":
    main()