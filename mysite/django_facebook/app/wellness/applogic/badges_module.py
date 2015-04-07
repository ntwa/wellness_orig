from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr


db = create_engine(connstr,pool_size=20, max_overflow=0)
Base = declarative_base()

       
class Badges(Base):
    __tablename__="badges"
    rank=Column(Integer, primary_key=True)
    badgename = Column(String(50))
    #badges_url= Column(String(500))
    attained_badge = relationship("AttainedUserBadges", backref=backref("badges", order_by=rank))
    
    def __init__(self):
        pass
 

    #def __repr__(self):
    #    return str(self.intermediary_id)
    
class AttainedUserBadges(Base):
    __tablename__="attained_user_badges"
    id=Column(Integer, primary_key=True)
    intermediary_id=Column(String(50))  
    date_attained=Column(Date)
    badge_id = Column(Integer, ForeignKey("badges.rank"))
    status=Column(Boolean)
 
    
    def __init__(self,intermediary_id,date_attained,badge_id):
        self.intermediary_id=intermediary_id
        self.date_attained=date_attained
        self.badge_id=badge_id
        self.status=1
     
    def getIntermediaryId(self):
        return self.intermediary_id

Base.metadata.create_all(db)
