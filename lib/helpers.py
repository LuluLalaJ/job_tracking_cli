from db.models import Job, User, Application
from prettytable import PrettyTable
from sqlalchemy import func

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
    while True:
        new_user = input('Are you a new user? y/n; (Type "quit" to exit) \n')
        if (new_user.lower() == 'y'):
            print("Let's add you to the database!")
            first_name, last_name = enter_name()
            new_user = add_new_user(session, first_name, last_name)
            print("You're in the system! Here is your info:")
            return new_user
        elif (new_user.lower() == ('n')):
            print("Let's find you in the database!")
            first_name, last_name = enter_name()
            id = input("What's your user id? \n")
            existing_user = find_user_by_id(session, id)
            if existing_user and existing_user.first_name == first_name and existing_user.last_name == last_name:
                print('Welcome back!')
                return existing_user
            else:
                print("Ummm, I can't seem to find you!")
        elif new_user.lower() == "admin":
            run_admin()
        elif new_user.lower() == "quit":
            quit()
        else:
            print('--Invalid response--')

def run_admin():
    print("--Need to add admin functionality!--")

def find_user_by_id(session, id):
    user = session.query(User).filter(User.user_id == id).first()
    return user

def enter_name():
    while True:
        first_name = input("What's your first name? \n")
        last_name = input("What's your last name? \n")
        if len(first_name ) > 0 and len(last_name) > 0:
            return first_name.title(), last_name.title()
        elif first_name or last_name is "quit" or "exit":
            quit()
        else:
            print("Not a valid name. Please enter a string longer than 0 characters.")
            continue

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
    print('Please enter your choice: A, B, C, D, or E')
    choice = input().lower()
    if choice == "e" or choice == "quit":
        quit()
    if choice in ["a", "b", "c", "d"]:
        return choice
    else:
        print('--Invalid response--')
        return None

def process_choice(session, choice, user):
    if choice == "a":
        while True:
            print_viewing_options()
            viewing_option = check_viewing_option()
            jobs = get_jobs_by_options(session, viewing_option)
            print_job_table(jobs)
            add_app = check_add_app()
            if add_app:
                job_id = check_job_id(user, jobs)
                add_new_application(session, user, job_id)
                print(create_user_application_table(user))
                return
    if choice == "b":
        handle_application_sorting(user)
    if choice == "c":
        app_id = check_app_id(user)
        update_application_status(session, app_id)
        print(create_user_application_table(user))
        return
    if choice == "d":
        handle_remove_application(session, user)
        print(create_user_application_table(user))
        return

def handle_application_sorting(user):
    menu = f'How would you like to sort your applications? \n' \
        + f'A. by job title \n' \
        + f'B. by company \n' \
        + f'C. by location \n' \
        + f'D. by salary \n' \
        + f'E. by remote \n' \
        + f'F. by application status'
    print(menu)
    sorting = sorting_choice()
    process_sorting(sorting, user)

def sorting_choice():
    while True:
        print('Please choose a sorting method: A, B, C, D, E, or F')
        sorting_choice = input().lower()
        if sorting_choice in ["a", "b", "c", "d", "e", "f"]:
            return sorting_choice
        else:
            print('--Invalid response--')
            continue

def process_sorting(sorting, user):
    table = create_user_application_table(user)
    if sorting == "a":
        print("Filtering by: job title")
        print(table.get_string(sortby="job title"))
    if sorting == "b":
        print("Filtering by: company")
        print(table.get_string(sortby="company"))
    if sorting == "c":
        print("Filtering by: location")
        print(table.get_string(sortby="location"))
    if sorting == "d":
        print("Filtering by: salary")
        print(table.get_string(sortby="salary($)"))
    if sorting == "e":
        print("Filtering by: remote")
        print(table.get_string(sortby="remote"))
    if sorting == "f":
        print("Filtering by: application status")
        print(table.get_string(sortby="application status"))

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

#Helper functions for adding new applications
def print_job_table(jobs):
    job_table = PrettyTable()
    job_table.field_names = ["job id", "job title", "company", "location", "salary($)", "remote"]
    rows = []
    for job in jobs:
        job_record = [job.job_id, job.job_title, job.company, job.location, job.salary_in_usd, job.remote]
        rows.append(job_record)
    job_table.add_rows(rows)
    if rows:
        print('Here are all the available jobs!')
        print(job_table)
    else:
        print("There are no jobs available in the database!")

def print_viewing_options():
    viewing_options = f'How would you like to view the jobs in the database? \n' \
        + f'1. see ALL the jobs\n' \
        + f'2. see remote jobs\n' \
        + f'3. see on-site jobs\n' \
        + f'4. search jobs by salary\n' \
        + f'5. search jobs by location\n' \
        + f'6. search jobs by job title\n' \
        + f'7. search jobs by company' \

    print(viewing_options)

def check_viewing_option():
     while True:
            viewing_option = input('Enter your viewing id: \n')
            try:
                viewing_option = int(viewing_option)
                app_id_exists = viewing_option in range(1, 8)
                if app_id_exists:
                    return viewing_option
                else:
                    print('Viewing option must be between 1 through 8. pleaset try gain!')
            except ValueError:
                print('Invalid input. Please enter an integer value.')

def get_jobs_by_options(session, viewing_option):
    jobs = None
    if viewing_option == 1:
        jobs = session.query(Job).all()
    if viewing_option == 2:
        jobs = session.query(Job).filter_by(remote=True).all()
    if viewing_option == 3:
        jobs = session.query(Job).filter_by(remote=False).all()
    if viewing_option == 4:
        salary_min, salary_max = check_salary()
        jobs = session.query(Job).filter(Job.salary_in_usd.between(salary_min, salary_max)).all()
    if viewing_option == 5:
        location = input("Search by location: \n")
        jobs = session.query(Job).filter(Job.location.ilike(f'%{location}%')).all()
    if viewing_option == 6:
        title = input("Search by job title: \n")
        jobs = session.query(Job).filter(Job.job_title.ilike(f'%{title}%')).all()
    if viewing_option == 7:
        company = input("Search by company: \n")
        jobs = session.query(Job).filter(Job.company.ilike(f'%{company}%')).all()
    return jobs

def check_job_id(user, jobs):
    while True:
        job_id = input('Enter your job id: \n')
        try:
            job_id = int(job_id)
            job_id_exists = job_id in [job.job_id for job in jobs]
            user_active_job_ids = [app.job_id for app in user.applications if app.active]
            if job_id_exists and (job_id not in user_active_job_ids):
                return job_id
            if job_id_exists:
                print("You have already added this job app! Add something else!")
            else:
                print('This is not one of the above jobs. pleaset try gain!')
        except ValueError:
            print('Invalid input. Please enter an integer value.')

def add_new_application(session, user, job_id):
    new_app = Application(
        job_id=job_id,
        user_id =user.user_id,
        status="to be submitted",
        active=True
    )
    session.add(new_app)
    session.commit()
    print('The job is added to your application tracking file!')

def check_salary():
    salary_min = input('Please enter the minimum salary you want: \n')
    salary_max = input('Please enter the highest salary you want: \n')
    try:
        salary_min = int(salary_min)
        salary_max = int(salary_max)
        if 0 < salary_min < salary_max:
            return salary_min, salary_max
        else:
            print('Error: salary must be a positive integer and min salary must be smaller than max salary')
    except ValueError:
        print("Error: Salary must be an integer.")

def check_add_app():
    while True:
        answer = input('Do you want to: 1. add a job application or 2. return to the previous menu? \n')
        if answer == "1":
            return True
        if answer == "2":
            return False
        else:
            print('Invalid inut; try again!')
