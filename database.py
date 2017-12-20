import configparser
import pathlib

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from sqlalchemy import create_engine


class DBConfig:
    def __init__(self, config):
        try:
            self.host = config['DATABASE']['host']
            self.user = config['DATABASE']['user']
            self.password = config['DATABASE']['password']
            self.dbname = config['DATABASE']['dbname']
        except KeyError as err:
            DBConfigError('Not found config: %s' % str(err))


class Error(Exception):
    """Base class of Error."""
    pass


class DBConfigError(Error):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


config_file_path = pathlib.Path('config/database.conf')
config = configparser.ConfigParser()
if not config.read(config_file_path):
    raise DBConfigError('Not found config file: %s' % str(config_file_path.absolute()))

dbconf = DBConfig(config)
url = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % ( # python>=3.6ならフォーマット文字列使ったほうがいいかも
    dbconf.user,
    dbconf.password,
    dbconf.host,
    dbconf.dbname,
)
engine = create_engine(url, pool_recycle=14400)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
metadata = MetaData(engine)
Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
