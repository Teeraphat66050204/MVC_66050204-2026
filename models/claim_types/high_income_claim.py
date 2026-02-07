from models.claim_types.base_claim import Claim

class HighIncomeClaim(Claim):
    def calculate(self) -> float:
        return min(float(self.monthly_income) / 5.0, float(self.cap))
