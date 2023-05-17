from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import User, Job, Application
from helpers import (process_choice as f1)




if __name__ == '__main__':
    engine = create_engine(f"sqlite:///db/jobtracking.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    s = Session()

    user = s.query(User).filter(User.user_id == 6).first()
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    import ipdb
    ipdb.set_trace()
