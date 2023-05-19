from db.models import Job, Application
from prettytable import PrettyTable
from helpers import create_user_application_table, main_menu, c
from rich import print

def filter_jobs_add_applications(session, user):
    while True:
        print_viewing_options()
        jobs = get_jobs_by_options(session, user)
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
        c.print('Here are all the available jobs!', style="success")
        print(job_table)
    else:
        c.print("There are no jobs available in the database!", style="error")

def print_viewing_options():
    c.print("How would you like to view the jobs in the database?", style="prompt")
    viewing_options = f'A. see ALL the jobs\n' \
        + f'B. see remote jobs\n' \
        + f'C. see on-site jobs\n' \
        + f'D. search jobs by salary\n' \
        + f'E. search jobs by location\n' \
        + f'F. search jobs by job title\n' \
        + f'G. search jobs by company\n' \
        + f'H. return to the previous menu\n' \
        + f'I. quit the program'
    c.print(viewing_options, style="menu")

def get_jobs_by_options(session, user):
    c.print('Enter your choice:', style="prompt")
    viewing_option = input().lower()
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
        c.print("Search by location:", style="prompt")
        location = input()
        jobs = session.query(Job).filter(Job.location.ilike(f'%{location}%')).all()
    elif viewing_option == "f":
        c.print("Search by job title:", style="prompt")
        title = input()
        jobs = session.query(Job).filter(Job.job_title.ilike(f'%{title}%')).all()
    elif viewing_option == "g":
        c.print("Search by company:", style="prompt")
        company = input()
        jobs = session.query(Job).filter(Job.company.ilike(f'%{company}%')).all()
    elif viewing_option == "h":
        main_menu(session, user)
    elif viewing_option == "i":
        quit()
    else:
        c.print('Invalid input. Please enter a valid letter.', style="error")
        filter_jobs_add_applications(session, user)
    return jobs

def check_job_id(user, jobs):
    while True:
        c.print("Enter your job id or [red]'Q'[/red] to return to the previous menu:", style="prompt")
        job_id = input().lower()
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
                    c.print("You have already added this job app! Add something else!", style="error")
                else:
                    c.print('This is not one of the above jobs. Please try again!', style="error")
            except ValueError:
                c.print('Invalid input. Please enter an integer value.', style="error")

def add_new_application(session, user, job_id):
    new_app = Application(
        job_id=job_id,
        user_id =user.user_id,
        status="to be submitted",
        active=True
    )
    session.add(new_app)
    session.commit()
    c.print('The job is added to your application tracking file!', style="success")

def check_salary():
    c.print('Please enter the minimum salary you want:', style="prompt")
    salary_min = input()
    c.print('Please enter the highest salary you want:', style="prompt")
    salary_max = input()
    try:
        salary_min = int(salary_min)
        salary_max = int(salary_max)
        if 0 < salary_min < salary_max:
            return salary_min, salary_max
        else:
            c.print('Error: salary must be a positive integer and min salary must be smaller than max salary', style="error")
    except ValueError:
        c.print("Error: Salary must be an integer.", style="error")

def check_add_app():
    while True:
        c.print('Do you want to:', style="prompt")
        c.print(f'A. add a job application \n' \
                + f'B. return to the previous menu', style="menu")
        answer = input().lower()
        if answer == "a":
            return True
        elif answer == "b":
            return False
        elif answer == "q":
            return
        else:
            c.print('Error: Please select A or B. Enter Q to return to previous menu', style="error")
