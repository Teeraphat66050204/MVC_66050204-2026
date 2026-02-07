from models.claim_types.base_claim import Claim

class LowIncomeClaim(Claim):
    def calculate(self) -> float:
        return 6500.0
