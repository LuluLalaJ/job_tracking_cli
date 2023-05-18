from db.models import Job, Application
from prettytable import PrettyTable
from sqlalchemy import func
from helpers import create_user_application_table
from rich import print
from rich.table import Table


def filter_jobs_add_applications(session, user):
    while True:
        print_viewing_options()
        viewing_option = check_viewing_option()
        if viewing_option == "go back to previous menu":
            return
        jobs = get_jobs_by_options(session, viewing_option)
        print_job_table(jobs)
        add_app = check_add_app()
        if add_app:
            job_id = check_job_id(user, jobs)
            if job_id:
                add_new_application(session, user, job_id)
                print(create_user_application_table(user))

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
        + f'A. see ALL the jobs\n' \
        + f'B. see remote jobs\n' \
        + f'C. see on-site jobs\n' \
        + f'D. search jobs by salary\n' \
        + f'E. search jobs by location\n' \
        + f'F. search jobs by job title\n' \
        + f'G. search jobs by company\n' \
        + f'H. return to the previous menu\n' \
        + f'I. quit the program'
    print(viewing_options)

def check_viewing_option():
    while True:
        viewing_option = input('Enter your choice: \n').lower()
        if viewing_option == "h":
            return "go back to previous menu"
        elif viewing_option == "i":
            quit()
        elif viewing_option in ["a", "b", "c", "d", "e", "f", "g"]:
            return viewing_option
        else:
            print('Invalid input. Please enter a valid letter.')

def get_jobs_by_options(session, viewing_option):
    jobs = None
    if viewing_option == "a":
        jobs = session.query(Job).all()
    elif viewing_option == "b":
        jobs = session.query(Job).filter_by(remote=True).all()
    elif viewing_option == "c":
        jobs = session.query(Job).filter_by(remote=False).all()
    elif viewing_option == "d":
        salary_min, salary_max = check_salary()
        jobs = session.query(Job).filter(Job.salary_in_usd.between(salary_min, salary_max)).all()
    elif viewing_option == "e":
        location = input("Search by location: \n")
        jobs = session.query(Job).filter(Job.location.ilike(f'%{location}%')).all()
    elif viewing_option == "f":
        title = input("Search by job title: \n")
        jobs = session.query(Job).filter(Job.job_title.ilike(f'%{title}%')).all()
    elif viewing_option == "g":
        company = input("Search by company: \n")
        jobs = session.query(Job).filter(Job.company.ilike(f'%{company}%')).all()
    return jobs

def check_job_id(user, jobs):
    while True:
        job_id = input("Enter your job id or 'Q' to return to the previous menu: \n").lower()
        if job_id == "q":
            return
        else:
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
    answer = input('Do you want to: \n' \
                + f'A. add a job application \n' \
                + f'B. return to the previous menu \n').lower()
    if answer == "a":
        return True
    if answer == "b":
        return False
    else:
        print('--Invalid input!--')
