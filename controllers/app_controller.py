from datetime import datetime

from models.auth_model import AuthModel
from models.claim_repo import ClaimRepo
from models.claimant_model import ClaimantModel
from models.compensation_repo import CompensationRepo
from models.policy_model import PolicyModel
from models.validators import valid_claim_id

from models.claim_types.claim_factory import build_claim_by_income


class AppController:
    def __init__(self, common_view, list_view, submit_view):
        self.v = common_view
        self.list_view = list_view
        self.submit_view = submit_view

    def run(self):
        while True:
            self.v.show_main_menu()
            choice = self.v.ask("Choose: ")

            if choice == "0":
                self.v.show_message("Bye!")
                break
            if choice == "1":
                self.citizen_flow()
            elif choice == "2":
                self.officer_flow()
            else:
                self.v.show_message("Invalid choice.")

    def citizen_flow(self):
        username = self.v.ask("Username: ")
        password = self.v.ask("Password: ")
        user = AuthModel.login(username, password)

        if not user or user[1] != "CITIZEN":
            self.v.show_error("Login failed (citizen).")
            return

        claimant_id = user[2]
        claimant = ClaimantModel.get_claimant(claimant_id)
        if claimant is None:
            self.v.show_error("Claimant not found.")
            return

        while True:
            self.show_claim_list_screen()
            print("\nS) Submit new claim")
            print("R) Refresh list")
            print("B) Back")
            cmd = self.v.ask("Choose: ").upper()

            if cmd == "B":
                return
            if cmd == "R":
                continue
            if cmd == "S":
                self.submit_claim_flow(claimant)
            else:
                self.v.show_message("Invalid option.")

    def officer_flow(self):
        username = self.v.ask("Username: ")
        password = self.v.ask("Password: ")
        user = AuthModel.login(username, password)

        if not user or user[1] != "OFFICER":
            self.v.show_error("Login failed (officer).")
            return

        while True:
            self.show_claim_list_screen()
            print("\nB) Back")
            cmd = self.v.ask("Choose: ").upper()
            if cmd == "B":
                return

    def show_claim_list_screen(self):
        claims = ClaimRepo.list_claims()
        comp_lookup = {}
        for row in claims:
            claim_id = row[0]
            comp = CompensationRepo.get_result(claim_id)
            if comp:
                comp_lookup[claim_id] = {"amount": comp[1], "date": comp[2]}
        self.list_view.show(claims, comp_lookup)

    def submit_claim_flow(self, claimant_row):
        claimant_id, _, _, monthly_income, _ = claimant_row

        self.submit_view.show_form()
        claim_id = self.v.ask("Claim ID (8 digits, first not 0): ")
        if not valid_claim_id(claim_id):
            self.v.show_error("Invalid claim_id format.")
            return

        submitted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cap = PolicyModel.get_cap()

        try:
            claim_model = build_claim_by_income(monthly_income, cap)
            amount = claim_model.calculate()

            self.submit_view.show_calculated(amount)
            ClaimRepo.create_claim(claim_id, claimant_id, submitted_date)
            CompensationRepo.save_result(
                claim_id=claim_id,
                amount=amount,
                calculated_date=submitted_date,
            )
            ClaimRepo.set_calculated(claim_id)

            self.v.show_message("Submitted and calculated successfully.")
        except Exception as exc:
            self.v.show_error(str(exc))

