def valid_claim_id(claim_id: str) -> bool:
    return (
        isinstance(claim_id, str)
        and len(claim_id) == 8
        and claim_id.isdigit()
        and claim_id[0] != "0"
    )
