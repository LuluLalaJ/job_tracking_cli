from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, MetaData, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

#need to understand what this naming convention is
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

#do I need this here???
engine = create_engine('sqlite:///jobtracking.db')

#This is just a practice
#Think about how you can be more specific about the data types/constraints/etc. for each column
class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer(), primary_key=True)
    job_title = Column(String())
    company = Column(String())
    location = Column(String())
    salary_in_usd = Column(Integer())
    remote = Column(Boolean())

    #still trying to understand back-populate & association_proxy
    applications = relationship('Application', back_populates="job")
    users = association_proxy('applications', 'user', creator=lambda user: Application(user=user))

    def __repr__(self):
        #edit the repr later if necessary
        return f'<Job: {self.job_title}; Company: {self.company}; Location: {self.location}; Salary: ${self.salary_in_usd}>'

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    #still trying to understand back-populate & association_proxy
    applications = relationship('Application', back_populates="user")
    jobs = association_proxy('applications', 'job', creator=lambda job: Application(job=job))

    def __repr__(self):
        return f'<User: {self.first_name} {self.last_name} | user_id: {self.user_id}>'

class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer(), primary_key=True)
    #https://learning.flatironschool.com/courses/6329/assignments/239678?module_item_id=563727
    #with dynamic default values like func.now(), one has to clear the data in the database before running new migration

    #maybe need to change this for testing? since seeding creates the same time stamps!
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    status = Column(String())
    active = Column(Boolean())

    job_id = Column(String(), ForeignKey("jobs.job_id"))
    user_id = Column(String(), ForeignKey("users.user_id"))

    #create relationships
    #Many-to-Many with an Association Object
    job = relationship('Job', back_populates='applications')
    user = relationship('User', back_populates='applications')

    def __repr__(self):
        return f'<Application: {self.job.job_title}; Status: {self.status}>'
