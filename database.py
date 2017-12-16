from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from sqlalchemy import create_engine


url = 'mysql+pymysql://root:gurutaminn1009@localhost/stay_and_analyzation?charset=utf8'
engine = create_engine(url, pool_recycle=14400)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
metadata = MetaData(engine)
Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
