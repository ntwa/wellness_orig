from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
Base = declarative_base()
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()
       
class Factors(Base):
    __tablename__="factors"
    factor_id = Column(String(50),primary_key=True)
    tree_factor=Column(Float)
    flower_factor=Column(Float)
    
    
    def __init__(self,factor_id,tree_factor,flower_factor):
        self.factor_id=factor_id
        self.tree_factor=tree_factor
        self.flower_factor=flower_factor
    @abstractmethod    
    def storeFactors(self):
        pass
    @abstractmethod
    def viewFactors(self):
        pass

    #def __repr__(self):
    #    return str(self.intermediary_id)

Base.metadata.create_all(db)
