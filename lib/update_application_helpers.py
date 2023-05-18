from db.models import Application
from rich import print
from helpers import c
from rich import print

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
        new_status = input('Select the new status: \n')
        try:
            new_status = int(new_status)
            if new_status == len(APPLICATION_STATUS) + 1:
                return
            if new_status == len(APPLICATION_STATUS) + 2:
                quit()
            if new_status in range (1, len(APPLICATION_STATUS) + 1):
                app = session.query(Application).filter_by(application_id = app_id)
                app.update({
                    'status': APPLICATION_STATUS[new_status-1]
                })
                session.commit()
                c.print('The application status is updated!', style="success")
                break
            else:
                c.print('Invalid input. Please enter an interger between 1 and 8.', style="error")
        except ValueError:
            c.print('Invalid input. Please enter an integer value.', style="error")

def print_app_status_menu():
    print('Valid status options:')
    i = 1
    for status in APPLICATION_STATUS:
        c.print(f'{i}. {status.title()}', style="menu")
        i += 1
    c.print(f'{i}. No change! Go back to the main menu', style="menu")
    c.print(f'{i+1}. Exit the program', style="menu")
