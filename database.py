from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *


url = 'mysql+pymysql://root:gurutaminn1009@localhost/stay-and-analyzation?charset=utf8'
engine = create_engine(url)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
metadata = MetaData(engine)
Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
