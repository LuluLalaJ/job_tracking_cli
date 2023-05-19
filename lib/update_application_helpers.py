from db.models import Application
from rich import print
from helpers import c


APPLICATION_STATUS = [
    "to be submitted",
    "submitted",
    "pending",
    "under review",
    "interview scheduled",
    "approved",
    "denied"
    ]

def update_application_status(session, app_id):
    while True:
        print_app_status_menu()
        c.print('Select the new status:', style="prompt")
        new_status = input().lower()

        if new_status == "h":
            quit()
        if new_status == "g":
            return
        if new_status in ["a", "b", "c", "d", "e", "f"]:
            if new_status == "a":
                updated_status = "to be submitted"
            if new_status == "b":
                updated_status = "submitted"
            if new_status == "c":
                updated_status = "pending"
            if new_status == "d":
                updated_status = "under review"
            if new_status == "e":
                updated_status = "interview scheduled"
            if new_status == "f":
                updated_status = "approved"

            app = session.query(Application).filter_by(application_id = app_id).first()
            old_status = app.status
            app.status = updated_status
            session.commit()

            app = session.query(Application).filter_by(application_id = app_id).first()

            c.print('The application status is updated!', style="success")
            c.print(f'Old Status: {old_status} ==> New Status: {app.status}', style="success")
            return
        else:
            c.print('Invalid option', style="error")

def print_app_status_menu():
    c.print('Valid status options:', style="prompt")
    status_menu = f'A. to be submitted \n' \
            + f'B. submitted \n' \
            + f'C. pending \n' \
            + f'D. under review \n' \
            + f'E. interview scheduled \n' \
            + f'F. approved \n' \
            + f'G. No change! Go back to the main menu \n' \
            + f'H. Exit the program'

    c.print(status_menu, style="menu")
