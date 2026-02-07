from datetime import datetime

from models.auth_model import AuthModel
from models.claim_repo import ClaimRepo
from models.claimant_model import ClaimantModel
from models.compensation_repo import CompensationRepo
from models.policy_model import PolicyModel
from models.validators import valid_claim_id

from models.claim_types.claim_factory import build_claim_by_income


class GuiController:
    def __init__(self, view):
        self.view = view
        self.current_user = None
        self.current_role = None
        self.current_claimant = None
        self._wire_events()
        self._set_logged_out_state()
        self.refresh_claims()

    def _wire_events(self):
        self.view.login_button.clicked.connect(self.handle_login)
        self.view.logout_button.clicked.connect(self.handle_logout)
        self.view.refresh_button.clicked.connect(self.refresh_claims)
        self.view.submit_button.clicked.connect(self.handle_submit_claim)
        self.view.view_list_button.clicked.connect(self.view.show_list_page)
        self.view.back_to_submit_button.clicked.connect(self.handle_go_submit)

    def _set_logged_out_state(self):
        self.current_user = None
        self.current_role = None
        self.current_claimant = None
        self.view.set_session_text("Not logged in")
        self.view.set_submit_enabled(False)
        self.view.show_list_page()

    def handle_login(self):
        role_selected, username, password = self.view.read_credentials()
        if not username or not password:
            self.view.show_error("Please enter username and password.")
            return

        user = AuthModel.login(username, password)
        if not user:
            self.view.show_error("Login failed.")
            return

        _, role, claimant_id = user
        self.current_user = user
        self.current_role = role
        self.view.clear_credentials()

        if role == "CITIZEN":
            claimant = ClaimantModel.get_claimant(claimant_id)
            if claimant is None:
                self.view.show_error("Claimant not found.")
                self._set_logged_out_state()
                return
            self.current_claimant = claimant
            self.view.set_submit_enabled(True)
            self.view.set_session_text(f"Logged in: {username} ({role})")
            self.view.show_submit_page()
        else:
            self.current_claimant = None
            self.view.set_submit_enabled(False)
            self.view.set_session_text(f"Logged in: {username} ({role})")
            self.view.show_list_page()

        self.refresh_claims()
        if role != role_selected:
            self.view.show_info(f"Login successful. Role switched to {role}.")
            return
        self.view.show_info("Login successful.")

    def handle_logout(self):
        self._set_logged_out_state()
        self.view.clear_credentials()
        self.view.clear_claim_id()
        self.refresh_claims()

    def refresh_claims(self):
        if self.current_role == "OFFICER":
            claims = ClaimRepo.list_claims()
        elif self.current_role == "CITIZEN" and self.current_claimant:
            claims = ClaimRepo.list_claims_by_claimant(self.current_claimant[0])
        else:
            claims = []

        comp_lookup = {}
        for row in claims:
            claim_id = row[0]
            comp = CompensationRepo.get_result(claim_id)
            if comp:
                comp_lookup[claim_id] = {"amount": comp[1], "date": comp[2]}
        self.view.render_claims(claims, comp_lookup)

    def handle_submit_claim(self):
        if self.current_role != "CITIZEN" or not self.current_claimant:
            self.view.show_error("Citizen login is required to submit a claim.")
            return

        claim_id = self.view.read_claim_id()
        if not valid_claim_id(claim_id):
            self.view.show_error("Claim ID must be 8 digits and cannot start with 0.")
            return

        try:
            claimant_id, _, _, monthly_income, _ = self.current_claimant
            cap = PolicyModel.get_cap()
            claim_model = build_claim_by_income(monthly_income, cap)

            amount = claim_model.calculate()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ClaimRepo.create_claim(claim_id, claimant_id, now)
            CompensationRepo.save_result(claim_id=claim_id, amount=amount, calculated_date=now)
            ClaimRepo.set_calculated(claim_id)

            self.view.clear_claim_id()
            self.refresh_claims()
            self.view.show_list_page()
            self.view.show_info(f"Submitted and calculated successfully: {amount}")
        except Exception as exc:
            self.view.show_error(str(exc))

    def handle_go_submit(self):
        if self.current_role != "CITIZEN":
            self.view.show_error("Citizen login is required to open submit form.")
            return
        self.view.show_submit_page()
