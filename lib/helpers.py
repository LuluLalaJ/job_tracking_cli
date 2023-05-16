from db.models import Job, User, Application
from prettytable import PrettyTable

APPLICATION_STATUS = [
    "to be submitted",
    "submitted",
    "pending",
    "under review",
    "interview scheduled",
    "approved",
    "denied"
    ]

def validate_user(session):
    #how can I enable quit to exist anytime??
    new_user = input()
    if (new_user.lower() == 'y'):
        print("let's add you to the database!")
        first_name, last_name = enter_name()
        new_user = add_new_user(session, first_name, last_name)
        print("You're in the system! here's your info:")
        return new_user
    elif (new_user.lower() == ('n')):
        print("Let's find you in the database!")
        first_name, last_name = enter_name()
        print("What's your user id")
        id = input()
        existing_user = find_user_by_id(session, id)
        if existing_user and existing_user.first_name == first_name and existing_user.last_name == last_name:
            print('Welcome back!')
            return existing_user
        else:
            print("Ummm, I can't seem to find you")
            return None
    elif new_user.lower() == "quit":
        quit()
    else:
        print('Incorrect input')
        return None

def find_user_by_id(session, id):
    user = session.query(User).filter(User.user_id == id).first()
    return user

def enter_name():
    while True:
        first_name = ""
        last_name = ""

        print("What's your first name?")
        first_input = input()
        print("What's your last name?")
        last_input = input()

        if len(first_input ) > 0 and len(last_input) > 0:
            first_name = first_input
            last_name = last_input
            return first_name.title(), last_name.title()
        else:
            print("Not a valid name. Please enter a string longer than 0 characters.")
            continue

def add_new_user(session, first_name, last_name):
    if (isinstance(first_name, str) and isinstance(last_name, str)):
        fn = first_name.title()
        ln = last_name.title()
        n_user = User(first_name=fn, last_name=ln)
        session.add(n_user)
        #difference between commit and flush
        session.commit()
        return find_user_by_id(session, n_user.user_id)
    else:
        return None

def show_user_applications(user):
    x = PrettyTable()
    x.field_names = ["application id", "job title", "company", "location", "salary($)", "remote", "application status"]
    if isinstance(user, User):
        rows = []
        for app in user.applications:
            if app.active:
                job = app.job
                app_record = [app.application_id, job.job_title, job.company, job.location, job.salary_in_usd, job.remote, app.status]
                rows.append(app_record)
        x.add_rows(rows)
        if rows:
            print('Here are your current active applications:')
            print(x)
        else:
            print("You don't have any active applications!")
    else:
        return None

def menu_choice():
    print('Please enter your choice: A, B, C, D, or E')
    choice = input().lower()
    if choice == "e" or choice == "quit":
        quit()
    if choice in ["a", "b", "c", "d"]:
        return choice
    else:
        print('The entered value is not valid!')
        return None

def process_choice(session, choice, user):
    if choice == "a":
        pass
    if choice == "b":
        pass
    if choice == "c":
        app_id = check_app_id(user)
        update_application_status(session, app_id)
        show_user_applications(user)
        return

    if choice == "d":
        print("Please enter the id of the application that you wish to delete:")
        application_id = input()
        #same as the comment on choice c validating application_id
        deactivate_application(session, int(application_id))
        show_user_applications(user)
        return None

def deactivate_application(session, app_id):
    app = session.query(Application).filter(Application.application_id == app_id)
    app.update({
        'active': False
    })
    session.commit()
    print('The application is deleted!')

def check_app_id(user):
    while True:
            app_id = input('Enter your app id: \n')
            try:
                app_id = int(app_id)
                app_id_exists = app_id in user_active_app_id(user)
                if app_id_exists:
                    return app_id
                else:
                    print('App ID does not exist in DB. pleaset try gain!')
            except ValueError:
                print('Invalid input. Please enter an integer value.')

def user_active_app_id(user):
    applications = user.applications
    return [app.application_id for app in applications]

def update_application_status(session, app_id):
    while True:
        print_app_status_menu()
        new_status = input('Select the new status: \n')
        try:
            new_status = int(new_status)
            if new_status == len(APPLICATION_STATUS) + 1:
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
    print(f'{i}. exist the program')
