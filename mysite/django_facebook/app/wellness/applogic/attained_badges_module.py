from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr


db = create_engine(connstr,pool_size=20, max_overflow=0)
Base = declarative_base()

       
class AttainedBadges(Base):
    __tablename__="badges"
    rank=Column(Integer, primary_key=True)
    badgename = Column(String(50))
    
    
    
    def __init__(self):
        pass
    @abstractmethod    
    def storePoints(self):
        pass
    @abstractmethod
    def viewPoints(self):
        pass
    @abstractmethod
    def drawChart(self):
        pass
    #def __repr__(self):
    #    return str(self.intermediary_id)

Base.metadata.create_all(db)