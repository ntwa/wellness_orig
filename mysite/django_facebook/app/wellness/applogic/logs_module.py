from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float,Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       
class Logs(Base):
    __tablename__="logs"
    id=Column(Integer, primary_key=True)
    intermediary_id = Column(String(50))
    clickscounter=Column(Integer)
    datecaptured = Column(Date)
    timecaptured=Column(Time)
    
    
    def __init__(self,intermediary_id,clickscounter,datecaptured,timecaptured):
        self.datecaptured=datecaptured
        self.intermediary_id=intermediary_id
        self.clickscounter=clickscounter
        self.timecaptured=timecaptured
    @abstractmethod    
    def storeLogs(self):
        pass
    @abstractmethod
    def viewLogs(self):
        pass
    @abstractmethod
    def drawChart(self):
        pass
    def __repr__(self):
        return str(self.intermediary_id)

Base.metadata.create_all(db)
