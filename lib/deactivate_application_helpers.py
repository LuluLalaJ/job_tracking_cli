
def handle_remove_application(session, user):
    while True:
        c.print("Enter the id of the application you wish to delete or [red]'Q'[/red] to return to last menu", style="prompt")
        application_id = input().lower()
        if application_id == "q" or application_id == "quit":
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


from db.models import Application
from helpers import c
from update_application_helpers import user_active_app_id
