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


class PilotCommencement(Base):
    __tablename__="pilot_commencement"
    datestarted=Column(Date, primary_key=True)
 

    #def getUrl(self):
    #    return str(self.intermediary_id)

Base.metadata.create_all(db)
#conn=db.connect()
