from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()
#db = create_engine('mysql://root:ugnkat@localhost/wellness')
Base = declarative_base()
#db = create_engine('mysql://root:ugnkat@localhost/wellness',)
       
class PhysicalActivity(Base):
    __tablename__="physical_activity"
    id=Column(Integer, primary_key=True)
    beneficiary_id = Column(Integer)
    datecaptured= Column(Date)
    starttimecaptured= Column(String(10))
    endtimecaptured= Column(String(10))
    stepscounter=Column(Integer)
    def __init__(self,beneficiary_id,datecaptured,starttimecaptured,endtimecaptured,stepscounter):
        self.beneficiary_id=beneficiary_id
        self.datecaptured=datecaptured
        self.starttimecaptured=starttimecaptured
        self.endtimecaptured=endtimecaptured
        self.stepscounter=stepscounter  
        
    def storeActivityPattern(self):
        pass
    
    def viewActivityPattern(self):
        pass
    
    def drawChart(self):
        pass
    #def __repr__(self):
    #    return str(self.beneficiary_id)


Base.metadata.create_all(db)
