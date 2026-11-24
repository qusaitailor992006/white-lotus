import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "white_lotus.db"
BACKUPS_DIR = BASE_DIR / "backups"

def backup_database():
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        print(f"[Error] Source database {DB_PATH} does not exist.")
        return False

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUPS_DIR / f"white_lotus_backup_{timestamp}.db"

    # Use SQLite online backup API to ensure zero corruption even under write load
    try:
        src = sqlite3.connect(str(DB_PATH))
        dst = sqlite3.connect(str(backup_file))
        with dst:
            src.backup(dst, pages=100)
        dst.close()
        src.close()

        # Run integrity check on backup file
        verify_conn = sqlite3.connect(str(backup_file))
        cursor = verify_conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        check_result = cursor.fetchone()
        verify_conn.close()

        if check_result and check_result[0] == "ok":
            size_kb = round(backup_file.stat().st_size / 1024, 2)
            print(f"[Backup Success] Created verified backup: {backup_file.name} ({size_kb} KB)")
        else:
            print(f"[Warning] Integrity check result: {check_result}")

        # Rotate: keep latest 10 backups
        all_backups = sorted(BACKUPS_DIR.glob("white_lotus_backup_*.db"), key=os.path.getmtime)
        if len(all_backups) > 10:
            for old in all_backups[:-10]:
                old.unlink()
                print(f"[Rotation] Removed old backup: {old.name}")

        return True

    except Exception as e:
        print(f"[Backup Error] Failed to create backup: {e}")
        return False

if __name__ == "__main__":
    backup_database()
