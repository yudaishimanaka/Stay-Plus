from sqlalchemy import *
from database import Base


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    mac_address = Column(String(17), unique=True, nullable=False)
    avatar = Column(String(255), nullable=True)

    def __repr__(self):
        return "<User('{}')>".format(self.user_id)
