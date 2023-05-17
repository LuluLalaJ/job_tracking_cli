from db.models import Job, User, Application
from prettytable import PrettyTable
from sqlalchemy import func

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
        + f'7. search jobs by company\n' \
        + f'8. return to the previous menu\n' \
        + f'9. quit the program\n'

    print(viewing_options)

def check_viewing_option():
     while True:
            viewing_option = input('Enter your viewing id: \n')
            try:
                viewing_option = int(viewing_option)
                app_id_exists = viewing_option in range(1, 10)
                if viewing_option == 9:
                    quit()
                if viewing_option == 8:
                    return "go back to previous menu"
                if app_id_exists:
                    return viewing_option
                else:
                    print('Viewing option must be between 1 through 9. pleaset try gain!')
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
