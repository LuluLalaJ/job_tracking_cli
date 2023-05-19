from db.models import User
from rich import print
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helpers import (create_user_application_table)

if __name__ == '__main__':
    engine = create_engine("sqlite:///db/jobtracking.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    user1 = session.query(User).get(2)
    print(create_user_application_table(user1))
