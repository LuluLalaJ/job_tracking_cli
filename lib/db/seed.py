#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Job, User, Application

# Figure out how to install Faker and Prettytable for users automatically with pip install

fake = Faker()

engine = create_engine('sqlite:///jobtracking.db')
Session = sessionmaker(bind=engine)
session = Session()

def clear_data():
    session.query(Job).delete()
    session.query(User).delete()
    session.query(Application).delete()
    session.commit()

def create_users():
    users = []
    for _ in range(10):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        users.append(user)

    session.add_all(users)
    session.commit()
    return users

def create_jobs():
    jobs = []
    for _ in range(30):
        job = Job(
            job_title=fake.job(),
            company=fake.company(),
            location=fake.city(),
            salary_in_usd=random.randint(50000, 200000),
            remote = random.choice([True, False])
        )
        jobs.append(job)

    session.add_all(jobs)
    session.commit()
    return jobs

APPLICATION_STATUS = [
    "to be submitted",
    "submitted",
    "pending",
    "under review",
    "interview scheduled",
    "approved",
    "denied"
    ]

def create_applications():
    applications = []
    for _ in range(100):
        application = Application(
            status = random.choice(APPLICATION_STATUS),
            active = random.choice([True, False])
        )
        applications.append(application)

    session.add_all(applications)
    session.commit()
    return applications

def relate_one_to_many(jobs, users, applications):
    for application in applications:
        application.job = random.choice(jobs)
        application.user = random.choice(users)

    session.add_all(applications)
    session.commit()
    return jobs, users, applications

if __name__ == "__main__":
    clear_data()
    jobs = create_jobs()
    users = create_users()
    applications = create_applications()
    jobs, users, applications = relate_one_to_many(jobs, users, applications)
