from models.claim_types.high_income_claim import HighIncomeClaim
from models.claim_types.low_income_claim import LowIncomeClaim
from models.claim_types.normal_claim import NormalClaim


def build_claim_by_income(monthly_income: float, cap: float):
    income = float(monthly_income)
    if income < 6500:
        return LowIncomeClaim(income, cap)
    if income >= 50000:
        return HighIncomeClaim(income, cap)
    return NormalClaim(income, cap)

