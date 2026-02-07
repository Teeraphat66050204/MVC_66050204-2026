from db import init_db, reset_data, seed_data

def main():
    init_db()
    reset_data()
    seed_data()

    try:
        from PySide6.QtWidgets import QApplication

        from controllers.gui_controller import GuiController
        from views.main_window_view import MainWindowView

        app = QApplication([])
        view = MainWindowView()
        controller = GuiController(view)
        app._controller = controller
        view.show()
        app.exec()
    except ImportError:
        from controllers.app_controller import AppController
        from views.claim_list_view import ClaimListView
        from views.common_view import CommonView
        from views.submit_claim_view import SubmitClaimView

        controller = AppController(
            common_view=CommonView(),
            list_view=ClaimListView(),
            submit_view=SubmitClaimView()
        )
        controller.run()

if __name__ == "__main__":
    main()
