from db.models import Job, User, Application
from prettytable import PrettyTable
from sqlalchemy import func
from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "menu": "cyan1",
    "error": "bold red3",
    "success": "light_green",
    "prompt": "cornsilk1"
})
c = Console(theme=custom_theme)

def validate_user(session):
    while True:
        c.print("Are you a new user? Y/N; (Type [red]'quit'[/red] to exit)", style="menu")
        new_user = input().lower()
        if (new_user == 'y'):
            c.print("Let's add you to the database!", style="success")
            first_name, last_name = enter_name()
            new_user = add_new_user(session, first_name, last_name)
            c.print("You're in the system! Here is your info:", style="success")
            return new_user
        elif (new_user == ('n')):
            c.print("Let's find you in the database!", style="success")
            first_name, last_name = enter_name()
            c.print("What's your user id?", style="prompt")
            id = input()
            existing_user = find_user_by_id(session, id)
            if existing_user and existing_user.first_name == first_name and existing_user.last_name == last_name:
                c.print('Welcome back!', style="success")
                return existing_user
            else:
                c.print("Ummm, I can't seem to find you!", style="error")
        elif new_user == "admin":
            #all admin functions are in admin.py
            c.print("Welcome, Admin!", style="success")
            run_admin(session)
        elif new_user == "quit" or new_user == "q":
            quit()
        else:
            c.print('--Invalid response--', style="error")

def main_menu(session, validated_user):
    while True:
        c.print('You can:', style="menu")
        menu = f'A. add a new job application \n' \
            + f'B. view/sort my applications \n' \
            + f'C. update an existing job application status \n' \
            + f'D. delete an existing job application \n' \
            + f'E. exit the program'
        c.print(menu, style="menu")
        choice = menu_choice()
        if choice:
            done_processing = process_choice(session, choice, validated_user)
            choice = done_processing

def find_user_by_id(session, id):
    user = session.query(User).filter(User.user_id == id).first()
    return user

def enter_name():
    while True:
        c.print("What's your first name?", style="prompt")
        first_name = input()
        c.print("What's your last name?", style="prompt")
        last_name = input()
        if len(first_name ) > 0 and len(last_name) > 0:
            return first_name.title(), last_name.title()
        elif first_name == "quit" or last_name == "quit":
            quit()
        else:
            c.print("Not a valid name. Please enter a string longer than 0 characters.", style="error")

def add_new_user(session, first_name, last_name):
    fn = first_name
    ln = last_name
    n_user = User(first_name=fn, last_name=ln)
    session.add(n_user)
    #difference between commit and flush
    session.commit()
    return find_user_by_id(session, n_user.user_id)

def create_user_application_table(user):
    application_table = PrettyTable()
    application_table.field_names = ["application id", "job title", "company", "location", "salary($)", "remote", "application status"]
    if isinstance(user, User):
        rows = []
        for app in user.applications:
            if app.active:
                job = app.job
                app_record = [app.application_id, job.job_title, job.company, job.location, job.salary_in_usd, job.remote, app.status]
                rows.append(app_record)
        application_table.add_rows(rows)
        return application_table
    else:
        return None

def menu_choice():
    c.print('Please enter your choice: A, B, C, D, or E', style="prompt")
    choice = input().lower()
    if choice == "e" or choice == "quit":
        quit()
    if choice in ["a", "b", "c", "d"]:
        return choice
    else:
        c.print('--Invalid response--', style="error")
        return None

def process_choice(session, choice, user):
    if choice == "a":
        filter_jobs_add_applications(session, user)

    if choice == "b":
        handle_application_sorting(user, session)

    if choice == "c":
        app_id = check_app_id(user)
        if not app_id:
            return
        update_application_status(session, app_id)
        print(create_user_application_table(user))

    if choice == "d":
        handle_remove_application(session, user)
        print(create_user_application_table(user))

def check_app_id(user):
    while True:
            c.print('Enter your app id or press "q" to return to the previous menu:', style="prompt")
            app_id = input().lower()
            if app_id == "q":
                return
            try:
                app_id = int(app_id)
                app_id_exists = app_id in user_active_app_id(user)
                if app_id_exists:
                    return app_id
                else:
                    c.print('App ID does not exist in DB. pleaset try gain!', style="error")
            except ValueError:
                c.print('Invalid input. Please enter an integer value.', style="error")

def user_active_app_id(user):
    applications = user.applications
    return [app.application_id for app in applications]

from add_application_helpers import filter_jobs_add_applications
from sort_application_helpers import handle_application_sorting
from update_application_helpers import update_application_status
from deactivate_application_helpers import handle_remove_application
from admin import run_admin
