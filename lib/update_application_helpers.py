
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
        new_status = input()
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
                c.print('Invalid input. Please enter an interger between 1 and 9.', style="error")
        except ValueError:
            c.print('Invalid input. Please enter an integer value.', style="error")

def print_app_status_menu():
    c.print('Valid status options:', style="prompt")
    i = 1
    for status in APPLICATION_STATUS:
        c.print(f'{i}. {status.title()}', style="menu")
        i += 1
    c.print(f'{i}. No change! Go back to the main menu', style="menu")
    c.print(f'{i+1}. Exit the program', style="menu")

def check_app_id(user, session):
    while True:
            c.print("Enter your app id or press [red]'0'[/red] to return to the previous menu:", style="prompt")
            app_id = input()
            try:
                app_id = int(app_id)
                if app_id == 0:
                    main_menu(session, user)
                else:
                    app_id_exists = app_id in user_active_app_id(user)
                    if app_id_exists or app_id == 0:
                        return app_id
                    else:
                        c.print('App ID does not exist in DB. Please try again!', style="error")
            except ValueError:
                c.print('Invalid input. Please enter an integer value.', style="error")

def user_active_app_id(user):
    applications = user.applications
    return [app.application_id for app in applications]


from db.models import Application
from helpers import c, main_menu