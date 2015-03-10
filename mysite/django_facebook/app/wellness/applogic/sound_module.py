from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       
class Sound(Base):
    __tablename__="soundlink"
    id=Column(Integer, primary_key=True)
    url = Column(String(255))
    
    
    def __init__(self,url):
        self.url=url
     
    @abstractmethod    
    def storeSound(self):
        pass
    @abstractmethod
    def viewSound(self):
        pass
    def __repr__(self):
        return str(self.url)
Base.metadata.create_all(db)
