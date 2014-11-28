from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine('mysql://root:ugnkat@localhost/wellness',poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       
class Points(Base):
    __tablename__="points"
    id=Column(Integer, primary_key=True)
    intermediary_id = Column(String(50))
    scoredpoints=Column(Integer)
    datecaptured = Column(Date)
    
    
    def __init__(self,intermediary_id,scoredpoints,datecaptured):
        self.datecaptured=datecaptured
        self.intermediary_id=intermediary_id
        self.scoredpoints=scoredpoints
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
