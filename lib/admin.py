from db.models import Job, User, Application
from prettytable import PrettyTable
from helpers import validate_user, main_menu, create_user_application_table

def run_admin(session):
    while True:
        menu = f'What would you like to do? \n' \
              + f'A. view all jobs \n' \
              + f'B. add a new job \n' \
              + f'C. edit an existing job \n' \
              + f'D. remove a job from the database \n' \
              + f'E. view all users \n' \
              + f'F. remove a user from the database \n' \
              + f'G. exit to main menu'
        print(menu)
        admin_choice(session)

def admin_choice(session):
    choice = input('Please enter your choice: A, B, C, D, E, F or G \n').lower()
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
        print('--Invalid response--')

def show_job_table(session):
    job_table = PrettyTable()
    job_table.field_names = ["job id", "job title", "company", "location", "salary", "remote"]
    rows = []
    jobs = session.query(Job).all()
    for job in jobs:
            job_record = [job.job_id, job.job_title, job.company, job.location, job.salary_in_usd, job.remote]
            rows.append(job_record)
    job_table.add_rows(rows)
    print('Here are all current jobs in the database:')
    print(job_table)

def add_job_to_db(session):
    job_title = input("Job Title: ").title()
    company = input("Company: ").title()
    location = input("Location: ").title()
    salary = input("Salary: ")
    remote = input("Remote (True/False): ").title()

    try:
        if remote == "True" or remote == "False":
            if remote == "True":
                remote = 1
            if remote == "False":
                remote = 0
            new_job = Job(
                job_title=job_title,
                company=company,
                location=location,
                salary_in_usd=int(salary),
                remote=bool(remote))
            session.add(new_job)
            session.commit()
            print('Job has been added to the database')
        else:
            print('Remote must be True or False')
    except ValueError:
        print('Salary must be an integer value')


def edit_job_in_db(session):
    job_id = input("Enter the ID of the job you want to edit: ")
    job = session.query(Job).filter_by(job_id=job_id).first()
    if job:
        job_title = input("Enter the updated Job Title: ").title()
        company = input("Enter the updated Company: ").title()
        location = input("Enter the updated Location: ").title()
        salary = input("Enter the updated Salary: ")
        remote = input("Enter the updated Remote (True/False): ").title()

        try:
            if remote == "True":
                remote = 1
            elif remote == "False":
                remote = 0
            else:
                print("Remote must be 'True' or 'False'")
                return
            bool(remote)
        except ValueError:
            print("Remote must be 'True' or 'False'")
            return

        try:
            valid_salary = int(salary)
        except ValueError:
            print('Salary must be an integer value')
            return

        if valid_salary <= 0:
            print("Salary must be a positive integer.")
            return
        else:
            job.job_title = job_title
            job.company = company
            job.location = location
            job.salary_in_usd = valid_salary
            job.remote = bool(remote)

            session.commit()
            print("Row updated successfully.")
                
    else:
        print("Row not found.")

def delete_job_from_db(session):
    job_id = input("Enter the ID of the job you want to remove: \n")
    print(type(job_id))
    job = session.query(Job).get(job_id)
    if job:
        session.delete(job)
        session.commit()
        print("Job removed successfully.")
    else:
        print("Item not found.")

def show_users_table(session):
    users_table = PrettyTable()
    users_table.field_names = ["user id", "first name", "last name"]
    rows = []
    users = session.query(User).all()
    for user in users:
            user_record = [user.user_id, user.first_name , user.last_name]
            rows.append(user_record)
    users_table.add_rows(rows)
    print('Here are all current users in the database:')
    print(users_table)

def delete_user_from_db(session):
    user_id = input("Enter the ID of the user you want to remove: \n")

    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        print("User removed successfully.")
    else:
        print("Item not found.")
