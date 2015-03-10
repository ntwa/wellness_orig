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

       
class Weight(Base):
    __tablename__="weight"
    id=Column(Integer, primary_key=True)
    beneficiary_id = Column(Integer)
    weight=Column(Float)
    datecaptured = Column(Date)
    
    
    def __init__(self,beneficiary_id,weight,datecaptured):
        self.datecaptured=datecaptured
        self.beneficiary_id=beneficiary_id
        self.weight=weight
    @abstractmethod    
    def storeWeight(self):
        pass
    @abstractmethod
    def viewWeightself(self):
        pass
    @abstractmethod
    def drawChart(self):
        pass
    #def __repr__(self):
    #    return str(self.beneficiary_id)

Base.metadata.create_all(db)
