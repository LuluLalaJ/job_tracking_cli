from db.models import Application
from helpers import user_active_app_id

def handle_remove_application(session, user):
    while True:
        print("Please enter the id of the application that you wish to delete:")
        application_id = input()
        try:
            application_id = int(application_id)
            app_id_exists = application_id in user_active_app_id(user)
            if app_id_exists:
                deactivate_application(session, application_id)
                break
            else:
                print("Error: Application ID must be valid ID number.")
                continue
        except ValueError:
            print("Error: ID must be an integer.")

def deactivate_application(session, app_id):
    app = session.query(Application).filter(Application.application_id == app_id)
    app.update({
        'active': False
    })
    session.commit()
    print('The application is deleted!')
