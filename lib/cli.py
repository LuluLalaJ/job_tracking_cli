#!/usr/bin/env python3

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

    print('Welcome to job application tracker!')

    validated_user = validate_user(session)
    print(validated_user)
    print(create_user_application_table(validated_user))

    main_menu(session, validated_user)
