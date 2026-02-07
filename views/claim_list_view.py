class ClaimListView:
    def show(self, claims, comp_lookup):
        print("\n=== CLAIM LIST ===")
        if not claims:
            print("No claims.")
            return
        for row in claims:
            claim_id, claimant_id, submitted_date, status, fn, ln, income, ctype = row
            comp = comp_lookup.get(claim_id)
            comp_text = f"{comp['amount']} ({comp['date']})" if comp else "-"
            print(f"[{claim_id}] {fn} {ln} | income={income} | type={ctype} | status={status} | compensation={comp_text}")
