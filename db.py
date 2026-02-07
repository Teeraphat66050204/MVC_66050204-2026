import sqlite3

DB_NAME = "compensation.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_conn() as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS Claimants(
            claimant_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            monthly_income REAL NOT NULL,
            claimant_type TEXT NOT NULL CHECK(claimant_type IN ('NORMAL','LOW','HIGH'))
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Claims(
            claim_id TEXT PRIMARY KEY CHECK(length(claim_id)=8 AND substr(claim_id,1,1)!='0'),
            claimant_id TEXT NOT NULL,
            submitted_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('SUBMITTED','CALCULATED')),
            FOREIGN KEY(claimant_id) REFERENCES Claimants(claimant_id)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Policies(
            policy_id TEXT PRIMARY KEY,
            max_cap REAL NOT NULL,
            income_condition TEXT NOT NULL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Compensations(
            claim_id TEXT PRIMARY KEY,
            amount REAL NOT NULL,
            calculated_date TEXT NOT NULL,
            FOREIGN KEY(claim_id) REFERENCES Claims(claim_id)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('CITIZEN','OFFICER')),
            claimant_id TEXT,
            FOREIGN KEY(claimant_id) REFERENCES Claimants(claimant_id)
        )
        """)


def reset_data():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Compensations")
        c.execute("DELETE FROM Claims")
        c.execute("DELETE FROM Users")
        c.execute("DELETE FROM Claimants")
        c.execute("DELETE FROM Policies")

def seed_data():
    """ใส่นโยบาย + user ตัวอย่าง"""
    with get_conn() as conn:
        c = conn.cursor()

        policies = [
            ("P_LOW", 20000, "income < 6500 => 6500"),
            ("P_NORMAL", 20000, "6500 <= income < 50000 => income (cap 20000)"),
            ("P_HIGH", 20000, "income >= 50000 => income/5 (cap 20000)"),
        ]
        for p in policies:
            c.execute("INSERT OR IGNORE INTO Policies VALUES (?,?,?)", p)

        # ตัวอย่างประชาชน 3 คน (และผูก user)
        claimants = [
            ("C001", "Aom", "Siri", 5000, "LOW"),
            ("C002", "Bank", "Krit", 12000, "NORMAL"),
            ("C003", "Fah", "Nok", 80000, "HIGH"),
        ]
        for cl in claimants:
            c.execute("INSERT OR IGNORE INTO Claimants VALUES (?,?,?,?,?)", cl)

        users = [
            ("citizen1", "1234", "CITIZEN", "C001"),
            ("citizen2", "1234", "CITIZEN", "C002"),
            ("citizen3", "1234", "CITIZEN", "C003"),
            ("officer", "admin", "OFFICER", None),
        ]
        for u in users:
            c.execute("INSERT OR IGNORE INTO Users VALUES (?,?,?,?)", u)
