#!/usr/bin/env python3
# from prettytable import PrettyTable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#looking into different way of importing
# from db.models import Job, User, Application
from helpers import (validate_user,
                    create_user_application_table,
                    menu_choice, process_choice)

if __name__ == '__main__':
    engine = create_engine(f"sqlite:///db/jobtracking.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    print('Welcome to job application tracker!')

    validated_user = validate_user(session)
    print(validated_user)
    print(create_user_application_table(validated_user))

    while True:
        menu = f'You can: \n' \
              + f'A. add a new job application \n' \
              + f'B. filter my job applications \n' \
              + f'C. update an existing job application status \n' \
              + f'D. delete an existing job application \n' \
              + f'E. exit the program'
        print(menu)
        choice = menu_choice()
        if choice:
            done_processing = process_choice(session, choice, validated_user)
            choice = done_processing
