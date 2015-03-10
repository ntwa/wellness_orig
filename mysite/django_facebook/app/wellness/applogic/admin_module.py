from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)

#db = create_engine('mysql://root:ugnkat@localhost/wellness')

db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       

class UserAdmin(Base):
    __tablename__="adminapp_table"
    username = Column(String(50),primary_key=True)
    passwd= Column(String(50))
    
    def __init__(self,username,passwd):
        self.username=username
        self.passwd=passwd   
        
    def __repr__(self):
        return str(self.passwd)
    


Base.metadata.create_all(db)
