from db import get_conn

class ClaimantModel:
    @staticmethod
    def get_claimant(claimant_id: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT claimant_id, first_name, last_name, monthly_income, claimant_type
                FROM Claimants WHERE claimant_id=?
            """, (claimant_id,))
            return cur.fetchone()

    @staticmethod
    def create_claimant(claimant_id, first_name, last_name, monthly_income, claimant_type):
        with get_conn() as conn:
            conn.execute("""
                INSERT INTO Claimants(claimant_id, first_name, last_name, monthly_income, claimant_type)
                VALUES (?,?,?,?,?)
            """, (claimant_id, first_name, last_name, monthly_income, claimant_type))
