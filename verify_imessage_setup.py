import os
import sqlite3
import subprocess

def check_db_access():
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    print(f"Checking access to {db_path}...")
    if not os.path.exists(db_path):
        print(f"❌ {db_path} not found.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM message")
        count = cursor.fetchone()[0]
        print(f"✅ chat.db is readable. Total messages: {count}")
        conn.close()
        return True
    except sqlite3.OperationalError:
        print("❌ Permission denied accessing chat.db. Please grant Full Disk Access to your terminal/IDE.")
        return False
    except Exception as e:
        print(f"❌ Error accessing chat.db: {e}")
        return False

def check_osascript():
    print("Checking osascript execution...")
    try:
        result = subprocess.run(['osascript', '-e', 'return "Hello"'], capture_output=True, text=True)
        if result.returncode == 0 and "Hello" in result.stdout:
            print("✅ osascript is working.")
            return True
        else:
            print(f"❌ osascript failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running osascript: {e}")
        return False

if __name__ == "__main__":
    db_ok = check_db_access()
    osa_ok = check_osascript()
    
    if db_ok and osa_ok:
        print("\n✅ iMessage Setup Verification Passed!")
    else:
        print("\n❌ iMessage Setup Verification Failed. Please check permissions.")
