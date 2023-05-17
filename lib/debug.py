from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User


if __name__ == '__main__':
    engine = create_engine(f"sqlite:///db/jobtracking.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    result = session.query(User).all()


    import ipdb; ipdb.set_trace()