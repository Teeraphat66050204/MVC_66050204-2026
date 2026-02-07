from models.claim_types.base_claim import Claim

class NormalClaim(Claim):
    def calculate(self) -> float:
        return min(float(self.monthly_income), float(self.cap))
