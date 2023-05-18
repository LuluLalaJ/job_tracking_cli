from db.models import Application
from helpers import user_active_app_id
from rich import print
from helpers import c
from rich import print


def handle_remove_application(session, user):
    while True:
        print("Please enter the id of the application that you wish to delete or\n")
        print("'Q' to return to the previous menu:\n")
        application_id = input().lower()
        if application_id == "q":
            return
        try:
            application_id = int(application_id)
            app_id_exists = application_id in user_active_app_id(user)
            if app_id_exists:
                deactivate_application(session, application_id)
                break
            else:
                c.print("Error: Application ID must be valid ID number.", style="error")
                continue
        except ValueError:
            c.print("Error: ID must be an integer.", style="error")

def deactivate_application(session, app_id):
    app = session.query(Application).filter(Application.application_id == app_id)
    app.update({
        'active': False
    })
    session.commit()
    c.print('The application is deleted!', style="success")
