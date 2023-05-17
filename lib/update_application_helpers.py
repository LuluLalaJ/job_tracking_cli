from db.models import Application

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
                print('The application status is updated!')
                break
            else:
                print('Invalid input. Please enter an interger between 1 and 8.')
        except ValueError:
            print('Invalid input. Please enter an integer value.')

def print_app_status_menu():
    i = 1
    for status in APPLICATION_STATUS:
        print(f'{i}. {status.capitalize()}')
        i += 1
    print(f'{i}. No change! Go back to the main menu')
    print(f'{i+1}. Exist the program')
