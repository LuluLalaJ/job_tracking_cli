from db.models import Job, User, Application
from prettytable import PrettyTable
from sqlalchemy import func
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helpers import (
    validate_user,
    create_user_application_table,
    main_menu)


if __name__ == '__main__':
    engine = create_engine("sqlite:///db/jobtracking.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    user1 = session.query(User).get(2)
    print(create_user_application_table(user1))
