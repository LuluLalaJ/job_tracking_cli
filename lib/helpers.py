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
        print("let's find you in the database!")
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
    #need to add validation!
    print("What's your first name?")
    first_name = input()
    print("Waht's your last name?")
    last_name = input()
    return first_name.title(), last_name.title()

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
    print('Please enter a your choice: A, B, C, D, or E')
    choice = input().lower()
    if choice == "e" or choice == "quit":
        quit()
    if choice in ["a", "b", "c", "d"]:
        return choice
    else:
        print('The entered value is not valid!')
        return None

def all_active_app_ids(user):
    applications = user.applications
    return [app.application_id for app in applications]

def process_choice(session, choice, user):
    if choice == "a":
        pass
    if choice == "b":
        pass
    if choice == "c":
        print("Please enter the id of the application that you wish to update")
        application_id = input()
        #same issue, is there a way not to go back all the way to interacting_with_db
        #if app id is not valid but to enter allow users to enter the application id again?
        if int(application_id) not in all_active_app_ids(user):
            print('The application id is not valid')
            return None
        update_application_status(session, int(application_id))
        show_user_applications(user)
        return None 

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

#is there a way to add go back to the previous menu??
def update_application_status(session, app_id):
    print('Please select the new applicaiton status:')
    i = 1
    for status in APPLICATION_STATUS:
        print(f'{i}. {status.capitalize()}')
        i += 1
    print(f'{i}. exist the program')

    choice = input()
    #need to think about the type of choice before the following?

    if int(choice) == i or choice.lower() == 'quit':
        quit()
    if int(choice) in range(1, i):
        app = session.query(Application).filter(Application.application_id == app_id)
        app.update({
            'status': APPLICATION_STATUS[int(choice)-1]
        })
        session.commit()
        print('The application status is updated!')
    else:
        #maybe need to let the user to choose again
        print ("Invalid choice!")
        return None
