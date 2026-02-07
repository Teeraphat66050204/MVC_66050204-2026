from db import get_conn

class ClaimRepo:
    @staticmethod
    def list_claims():
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT cl.claim_id, cl.claimant_id, cl.submitted_date, cl.status,
                       p.first_name, p.last_name, p.monthly_income, p.claimant_type
                FROM Claims cl
                JOIN Claimants p ON p.claimant_id = cl.claimant_id
                ORDER BY cl.submitted_date DESC
            """)
            return cur.fetchall()

    @staticmethod
    def create_claim(claim_id: str, claimant_id: str, submitted_date: str):
        with get_conn() as conn:
            conn.execute("""
                INSERT INTO Claims(claim_id, claimant_id, submitted_date, status)
                VALUES (?,?,?, 'SUBMITTED')
            """, (claim_id, claimant_id, submitted_date))

    @staticmethod
    def list_claims_by_claimant(claimant_id: str):
        with get_conn() as conn:
            cur = conn.execute(
                """
                SELECT cl.claim_id, cl.claimant_id, cl.submitted_date, cl.status,
                       p.first_name, p.last_name, p.monthly_income, p.claimant_type
                FROM Claims cl
                JOIN Claimants p ON p.claimant_id = cl.claimant_id
                WHERE cl.claimant_id = ?
                ORDER BY cl.submitted_date DESC
                """,
                (claimant_id,),
            )
            return cur.fetchall()

    @staticmethod
    def set_calculated(claim_id: str):
        with get_conn() as conn:
            conn.execute("UPDATE Claims SET status='CALCULATED' WHERE claim_id=?", (claim_id,))
