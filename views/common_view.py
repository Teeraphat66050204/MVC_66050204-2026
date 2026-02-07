class CommonView:
    def ask(self, prompt: str) -> str:
        return input(prompt).strip()

    def show_error(self, msg: str):
        print(f"Error: {msg}")

    def show_message(self, msg: str):
        print(msg)

    def show_main_menu(self):
        print("\n=== Compensation System (MVC CLI) ===")
        print("1) Login (Citizen)")
        print("2) Login (Officer)")
        print("0) Exit")
