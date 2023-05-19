from db.models import Job, User
from prettytable import PrettyTable
from helpers import validate_user, main_menu, create_user_application_table, c

from rich import print

def run_admin(session):
    while True:
        menu = f'A. view all jobs \n' \
            + f'B. add a new job \n' \
            + f'C. edit an existing job \n' \
            + f'D. remove a job from the database \n' \
            + f'E. view all users \n' \
            + f'F. remove a user from the database \n' \
            + f'G. exit to main menu'
        c.print('What would you like to do?', style="prompt")
        c.print(menu, style="menu")
        admin_choice(session)

def admin_choice(session):
    c.print('Please enter your choice: A, B, C, D, E, F or G', style="prompt")
    choice = input().lower()
    if choice == "a":
        show_job_table(session)
    elif choice == "b":
        add_job_to_db(session)
    elif choice == "c":
        edit_job_in_db(session)
    elif choice == "d":
        delete_job_from_db(session)
    elif choice == "e":
        show_users_table(session)
    elif choice == "f":
        delete_user_from_db(session)
    elif choice == "g":
        validated_user = validate_user(session)
        print(validated_user)
        print(create_user_application_table(validated_user))
        main_menu(session, validated_user)
    else:
        c.print('Error: Please select a letter from A to G', style="error")

def show_job_table(session):
    job_table = PrettyTable()
    job_table.field_names = ["job id", "job title", "company", "location", "salary", "remote"]
    rows = []
    jobs = session.query(Job).all()
    for job in jobs:
            job_record = [job.job_id, job.job_title, job.company, job.location, job.salary_in_usd, job.remote]
            rows.append(job_record)
    job_table.add_rows(rows)
    c.print('Here are all current jobs in the database:', style="success")
    print(job_table)

def add_job_to_db(session):
    c.print("Job Title: ", end='', style="prompt")
    job_title = input().title()
    c.print("Company: ", end='', style="prompt")
    company = input().title()
    c.print("Location: ", end='', style="prompt")
    location = input().title()
    c.print("Salary: ", end='', style="prompt")
    salary = input()
    c.print("Remote (True/False): ", end='', style="prompt")
    remote = input().title()

    valid_salary = validate_salary(salary, session)
    valid_remote = validate_remote(remote, session)

    new_job = Job(
        job_title=job_title,
        company=company,
        location=location,
        salary_in_usd=valid_salary,
        remote=valid_remote)
    session.add(new_job)
    session.commit()

    c.print('Job has been added to the database', style="success")
    # ADD A PRINTING TABLE OF THE NEWLY ADDED JOB INFORMATION #

def edit_job_in_db(session):
    c.print("Enter the ID of the job you want to edit: ", style="prompt")
    job_id = input()
    job = session.query(Job).filter_by(job_id=job_id).first()
    if job:
        c.print("Enter the updated Job Title: ", end='', style="prompt")
        job_title = input().title()
        c.print("Enter the updated Company: ", end='', style="prompt")
        company = input().title()
        c.print("Enter the updated Location: ", end='', style="prompt")
        location = input().title()
        c.print("Enter the updated Salary: ", end='', style="prompt")
        salary = input()
        c.print("Enter the updated Remote (True/False): ", end='', style="prompt")
        remote = input().title()

        valid_salary = validate_salary(salary, session)
        valid_remote = validate_remote(remote, session)

        job.job_title = job_title
        job.company = company
        job.location = location
        job.salary_in_usd = valid_salary
        job.remote = valid_remote

        session.commit()

        c.print("Row updated successfully.", style="success")
        # ADD A PRINTING TABLE OF THE NEWLY EDITED JOB INFORMATION #
    else:
        c.print("Job ID not found.", style="error")

def validate_salary(value, session):
    try:
        value = int(value)
    except ValueError:
        c.print('Salary must be an integer.', style="error")
        run_admin(session)
    if value <= 0:
        c.print("Salary must be a positive integer.", style="error")
        run_admin(session)
    else:
        return value

def validate_remote(value, session):
    if value == "True":
        value = True
    elif value == "False":
        value = False
    else:
        c.print("Remote must be [red][bold]'True' or 'False'[/bold][/red]", style="error")
        run_admin(session)
    return value

def delete_job_from_db(session):
    c.print("Enter the ID of the job you want to remove:", style="prompt")
    job_id = input()
    job = session.query(Job).get(job_id)
    if job:
        session.delete(job)
        session.commit()
        c.print("Job removed successfully!", style="success")
    else:
        c.print("Item not found.", style="error")

def show_users_table(session):
    users_table = PrettyTable()
    users_table.field_names = ["user id", "first name", "last name"]
    rows = []
    users = session.query(User).all()
    for user in users:
            user_record = [user.user_id, user.first_name , user.last_name]
            rows.append(user_record)
    users_table.add_rows(rows)
    c.print('Here are all current users in the database:', style="success")
    print(users_table)

def delete_user_from_db(session):
    c.print("Enter the ID of the user you want to remove:", style="prompt")
    user_id = input()
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        c.print("User removed successfully!", style="success")
    else:
        c.print("Item not found.", style="error")
