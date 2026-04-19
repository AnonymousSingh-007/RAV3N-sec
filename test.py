#!/usr/bin/env python3
"""
VULNERABLE PYTHON SCRIPT - EDUCATIONAL DEMO ONLY
This is a deliberately insecure "SecureVault Pro" application.
It contains a mix of BIG and subtle vulnerabilities for learning purposes
(code review, pentesting practice, etc.). 
DO NOT run this on any real system, expose to the internet, or use in production.
"""

import os
import sys
import sqlite3
import hashlib
import random
import string
import subprocess
import pickle
import base64
import time
import logging
from datetime import datetime
from getpass import getpass

# =============================================
# BIG VULNERABILITIES - HARD-CODED SECRETS
# =============================================
HARDCODED_ADMIN_USER = "admin"
HARDCODED_ADMIN_PASS = "SuperSecret123!"          # obvious
API_KEY = "sk_live_9876543210abcdef1234567890"   # hardcoded API key (big)
ENCRYPTION_KEY = b"my_fixed_16_byte_key!!"       # weak symmetric key
DEBUG_MODE = True                                 # debug left on

# Subtle: fallback to hardcoded if env var missing
DATABASE_URL = os.getenv("VAULT_DB_URL", "sqlite:///vault.db")
LOG_FILE = "vault.log"

# Weak static salt for hashing (subtle)
WEAK_SALT = "static_salt_2026"

# Configure insecure logging (logs everything including secrets)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =============================================
# DATABASE SETUP (SQL Injection ready)
# =============================================
def init_database():
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    
    # BIG VULN: No parameterised queries anywhere
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT
        )
    """)
    
    # Insert default admin with weak hash if not exists
    admin_hash = hashlib.md5((HARDCODED_ADMIN_PASS + WEAK_SALT).encode()).hexdigest()
    cursor.execute(f"""
        INSERT OR IGNORE INTO users (username, password_hash, email, role, created_at)
        VALUES ('{HARDCODED_ADMIN_USER}', '{admin_hash}', 'admin@company.local', 'admin', '{datetime.now().isoformat()}')
    """)
    
    # Another table with sensitive data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value TEXT,
            owner TEXT
        )
    """)
    conn.commit()
    conn.close()

# =============================================
# AUTHENTICATION - MULTIPLE VULNS
# =============================================
def hash_password(password: str) -> str:
    # Subtle vuln: MD5 + static salt (collision prone, no PBKDF2)
    return hashlib.md5((password + WEAK_SALT).encode()).hexdigest()

def login_user(username: str, password: str):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    
    # BIG VULN: Classic SQL Injection (string concatenation)
    query = f"""
        SELECT id, username, role FROM users 
        WHERE username = '{username}' 
        AND password_hash = '{hash_password(password)}'
    """
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            logging.info(f"User {username} logged in successfully")  # subtle: logs username but could be more
            return {"id": user[0], "username": user[1], "role": user[2]}
        else:
            # Subtle timing attack possible (different sleep on failure)
            if username == HARDCODED_ADMIN_USER:
                time.sleep(0.3)
            else:
                time.sleep(0.1)
            return None
    except Exception as e:
        # BIG VULN: Information disclosure in error messages
        print(f"[DEBUG] Database error: {e}")
        logging.error(f"Login error: {e}")
        return None
    finally:
        conn.close()

# =============================================
# USER MANAGEMENT (more injection vectors)
# =============================================
def register_user(username: str, password: str, email: str):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    pw_hash = hash_password(password)
    
    # BIG VULN: SQL Injection in registration too
    try:
        cursor.execute(f"""
            INSERT INTO users (username, password_hash, email, created_at)
            VALUES ('{username}', '{pw_hash}', '{email}', '{datetime.now().isoformat()}')
        """)
        conn.commit()
        print(f"[+] User {username} registered!")
    except sqlite3.IntegrityError:
        print("[-] Username already exists")
    except Exception as e:
        print(f"[ERROR] {e}")  # info leak
    finally:
        conn.close()

def list_users(current_user):
    # Subtle: Only admins should see this, but no real check
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# =============================================
# COMMAND INJECTION EXAMPLE
# =============================================
def backup_database(user_input_path: str):
    # BIG VULN: Command injection via shell=True + user controlled input
    try:
        # Deliberately unsafe
        cmd = f"cp vault.db {user_input_path} && echo Backup complete"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Backup failed: {e}")

# =============================================
# INSECURE FILE OPERATIONS (Path Traversal)
# =============================================
def save_uploaded_file(filename: str, content: bytes):
    # BIG VULN: Path traversal + no validation
    safe_path = f"./uploads/{filename}"  # but filename can be ../../etc/passwd
    try:
        os.makedirs("./uploads", exist_ok=True)
        with open(safe_path, "wb") as f:  # actually unsafe
            f.write(content)
        print(f"[+] File saved as {safe_path}")
    except Exception as e:
        print(f"File save error: {e}")

def read_file(filename: str):
    # BIG VULN: Path traversal
    try:
        with open(f"./uploads/{filename}", "rb") as f:
            return f.read()
    except Exception as e:
        print(f"Read error: {e}")
        return b""

# =============================================
# INSECURE DESERIALIZATION
# =============================================
def save_config(config_data):
    # Subtle: using pickle on user-controlled data
    try:
        with open("config.pkl", "wb") as f:
            pickle.dump(config_data, f)
    except:
        pass

def load_config():
    # BIG VULN: Arbitrary code execution via pickle
    try:
        with open("config.pkl", "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Config load failed: {e}")
        return {}

# =============================================
# EVAL / EXEC VULN
# =============================================
def generate_custom_report(formula: str):
    # BIG VULN: eval on user input
    try:
        # Pretend this is a "report engine"
        result = eval(formula, {"__builtins__": {}}, {"x": 42, "y": 100})  # limited but still dangerous
        return result
    except Exception as e:
        return f"Report error: {e}"

# =============================================
# WEAK TOKEN GENERATION
# =============================================
def generate_session_token():
    # Subtle vuln: using random instead of secrets module
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(16))  # predictable with same seed

# =============================================
# MAIN APPLICATION LOOP
# =============================================
def main():
    init_database()
    print("=" * 60)
    print("🔒 SecureVault Pro v2.1 - Enterprise Edition")
    print("=" * 60)
    print("WARNING: This demo contains intentional vulnerabilities!")
    print()
    
    current_user = None
    session_token = None
    
    while True:
        print("\nMain Menu:")
        if not current_user:
            print("1. Login")
            print("2. Register")
            print("3. Exit")
        else:
            print(f"Logged in as: {current_user['username']} ({current_user['role']})")
            print("4. List all users")
            print("5. Create backup (path)")
            print("6. Upload file")
            print("7. Read file")
            print("8. Generate custom report (eval)")
            print("9. Load/save config (pickle)")
            print("10. View secrets")
            print("11. Logout")
        
        choice = input("\n> ").strip()
        
        if not current_user:
            if choice == "1":
                username = input("Username: ")
                password = getpass("Password: ")
                user = login_user(username, password)
                if user:
                    current_user = user
                    session_token = generate_session_token()
                    print(f"[+] Login successful! Session token: {session_token}")
                    # Subtle: token is predictable and never invalidated
                else:
                    print("[-] Invalid credentials")
            elif choice == "2":
                username = input("New username: ")
                password = getpass("Password: ")
                email = input("Email: ")
                register_user(username, password, email)
            elif choice == "3":
                print("Goodbye!")
                break
        else:
            if choice == "4":
                users = list_users(current_user)
                for u in users:
                    print(u)
            elif choice == "5":
                path = input("Backup path (e.g. /tmp/backup.db): ")
                backup_database(path)   # command injection possible
            elif choice == "6":
                filename = input("Filename (can contain ../): ")
                content = input("File content: ").encode()
                save_uploaded_file(filename, content)
            elif choice == "7":
                filename = input("Filename to read: ")
                data = read_file(filename)
                print(data.decode(errors="ignore")[:500])
            elif choice == "8":
                formula = input("Enter report formula (e.g. x + y * 10): ")
                result = generate_custom_report(formula)
                print(f"Report result: {result}")
            elif choice == "9":
                if input("Save or load config? (s/l): ") == "s":
                    config = {"api_key": API_KEY, "debug": DEBUG_MODE}
                    save_config(config)
                    print("Config saved (pickle)")
                else:
                    cfg = load_config()
                    print("Loaded config:", cfg)
            elif choice == "10":
                # Subtle: leaks hardcoded secrets if you know the magic
                if current_user["role"] == "admin":
                    print(f"Internal API key: {API_KEY}")
                    print(f"Encryption key: {ENCRYPTION_KEY}")
                else:
                    print("Access denied (but actually still logged in debug)")
            elif choice == "11":
                current_user = None
                session_token = None
                print("Logged out")
            else:
                print("Invalid option")
        
        # Subtle race-condition like behaviour (sleep)
        time.sleep(0.2)

if __name__ == "__main__":
    # BIG VULN: runs with whatever privileges the user has
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting SecureVault Pro...")
    except Exception as e:
        # Final info leak
        print(f"Critical error (debug mode): {e}")
        import traceback
        traceback.print_exc()