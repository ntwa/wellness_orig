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

       
class Avatars(Base):
    __tablename__="avatars"
    id=Column(Integer, primary_key=True)
    avatar_url=Column(String(200))
    useravatars = relationship("UserAvatars",uselist=False, backref="avatars")
    
    
    def __init__(self,avatar_url):
        self.avatar_url=avatar_url

        
class UserAvatars(Base):
    __tablename__="useravatars"
    intermediary_id=Column(String(50),primary_key=True)
    
    avatar_id = Column(Integer, ForeignKey("avatars.id"))
    
    def __init__(self,intermediary_id,avatar_id):
        self.intermediary_id=intermediary_id
        self.avatar_id=avatar_id



    #def getUrl(self):
    #    return str(self.intermediary_id)

Base.metadata.create_all(db)
#conn=db.connect()