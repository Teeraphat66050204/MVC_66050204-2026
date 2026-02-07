from db import get_conn

class CompensationRepo:
    @staticmethod
    def save_result(claim_id: str, amount: float, calculated_date: str):
        with get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO Compensations(claim_id, amount, calculated_date)
                VALUES (?,?,?)
            """, (claim_id, amount, calculated_date))

    @staticmethod
    def get_result(claim_id: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT claim_id, amount, calculated_date
                FROM Compensations WHERE claim_id=?
            """, (claim_id,))
            return cur.fetchone()
