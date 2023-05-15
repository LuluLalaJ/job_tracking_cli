from db.models import Job, User, Application
from prettytable import PrettyTable

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
    x.field_names = ["job title", "company", "location", "salary($)", "remote", "application status"]
    if isinstance(user, User):
        rows = []
        for app in user.applications:
            if app.active:
                job = app.job
                app_record = [job.job_title, job.company, job.location, job.salary_in_usd, job.remote, app.status]
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

def process_choice():
    pass
