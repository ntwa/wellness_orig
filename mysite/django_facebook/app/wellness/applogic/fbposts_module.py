from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       
class ObjectActivity(Base):
    __tablename__="objectactivity"
   # id=Column(Integer, primary_key=True)
    message=Column(String(500))
    event_url= Column(String(255), primary_key=True)
    event_object=Column(String(50))
    object_owner=Column(String(255)) 
    date_of_display=Column(String(50))   
    pic=Column(String(255))
    event_type=Column(String(255),primary_key=True)
    message_title=Column(String(50))
    caption=Column(String(255))
    description=Column(String(255))
    counter=Column(Integer)
    old_counter=Column(Integer)    
    
    def __init__(self,message,event_url,event_object,object_owner,event_type,date_of_display,pic,message_title,caption,description,counter,old_counter):
        self.message=message
        self.event_url=event_url
        self.event_object=event_object
        self.object_owner=object_owner
        self.date_of_display=date_of_display
        self.event_type=event_type
        self.message_title=message_title
        self.pic=pic
        self.caption=caption
        self.description=description
        self.counter=counter
        self.old_counter=old_counter

Base.metadata.create_all(db)
