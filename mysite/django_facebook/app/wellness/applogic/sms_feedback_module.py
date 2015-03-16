from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()
Base = declarative_base()

       
class Feedback(Base):
    __tablename__="feedback"
    id=Column(Integer, primary_key=True)
    recipient_mobile=Column(String(20))
    message=Column(String(1000))
    status=Column(Boolean)
    
    
    
    def __init__(self,recipient_mobile,message):
        self.recipient_mobile=recipient_mobile
        self.message=message
        self.status=0
    @abstractmethod    
    def storeFeddback(self):
        pass
    @abstractmethod
    def viewFeedback(self):
        pass

    #def __repr__(self):
    #    return str(self.intermediary_id)

Base.metadata.create_all(db)
