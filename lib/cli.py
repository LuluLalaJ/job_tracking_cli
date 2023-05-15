#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#looking into different way of importing
from db.models import Job, User, Application

def app():
    pass

if __name__ == '__main__':
    print('Welcome to job application tracker!')
    engine = create_engine(f"sqlite:///db/jobtracking.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    user1 = session.query(User).filter(User.user_id == 1).first()
    # print(user1)
    application1 = session.query(Application).filter(Application.application_id == 1).first()
    # job1 = session.query(Job).filter(Job.job_id == 1).first()

    print(application1.job)
    print(application1.user)
    # print(job1)
    # print(job1.applications)

    # print(session.query(Job).all())
    # print(session.query(User).all())
    # print(session.query(Application).all())
