from sqlalchemy.orm import sessionmaker, scoped_session

Session = scoped_session(sessionmaker())
