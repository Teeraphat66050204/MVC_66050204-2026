from db import get_conn

class PolicyModel:
    @staticmethod
    def get_cap() -> float:
        # ตามโจทย์ cap = 20000 (เก็บใน Policies เพื่อให้ “มีตารางนโยบายจริง”)
        with get_conn() as conn:
            cur = conn.execute("SELECT max_cap FROM Policies LIMIT 1")
            row = cur.fetchone()
            return float(row[0]) if row else 20000.0
