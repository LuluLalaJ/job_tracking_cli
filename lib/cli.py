#!/usr/bin/env python3
from prettytable import PrettyTable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#looking into different way of importing
from db.models import Job, User, Application
from helpers import (validate_user, show_user_applications,
                     menu_choice, process_choice)

if __name__ == '__main__':
    engine = create_engine(f"sqlite:///db/jobtracking.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    print('Welcome to job application tracker!')
    validating_user = True
    while validating_user:
        print('Are you a new user? y/n; enter "quit" to exist')
        validated_user = validate_user(session)
        if validated_user:
            print(validated_user)
            validating_user = False

    show_user_applications(validated_user)

    interacting_with_db = True
    while interacting_with_db:
        menu = f'You can: \n' \
              + f'A. add a new job application \n' \
              + f'B. filter my job applications \n' \
              + f'C. update an existing job application \n' \
              + f'D. delete an existing job application \n' \
              + f'E. exist the program'
        print(menu)
        choice = menu_choice()
        if choice:
            interacting_with_db = False

    process_choice(choice)

    # user1 = session.query(User).filter(User.user_id == 1).first()
    # print(user1)
    # application1 = session.query(Application).filter(Application.application_id == 1).first()
    # job1 = session.query(Job).filter(Job.job_id == 1).first()

    # print(application1.job)
    # print(application1.user)
    # print(job1)
    # print(job1.applications)

    # print(session.query(Job).all())
    # print(session.query(User).all())
    # print(session.query(Application).all())
