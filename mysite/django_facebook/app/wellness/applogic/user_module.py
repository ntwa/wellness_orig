from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.pool import NullPool

#db = create_engine('mysql://root:ugnkat@localhost/wellness')
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       
class Intermediary(Base):
    __tablename__="intermediaries"
    intermediary_id = Column(String(50),primary_key=True)
    intermediary_name=Column(String(50))
    password= Column(String(4))
    #beneficiary = relationship("Beneficiary", backref=backref("intermediaries", order_by=intermediary_id))
    beneficiary = relationship("Beneficiary", backref=backref("intermediaries", order_by="Beneficiary.beneficiary_id"))
    def __init__(self,intermediary_id,password):
        self.beneficiary_id=beneficiary_id
        self.password=password
        
    def setId(self):
        pass
    def setName(self):
        pass
    def setMobileNumber(self):
        pass
    def getId(self):
        pass
    def getName(self):
        pass
    def getMobileNumber(self):
        pass
    def sendEncouregement(self):
        pass
    def viewRewards(self):
        pass
    def __repr__(self):
        return str(self.intermediary_id)
       
class Beneficiary(Base):
    __tablename__="beneficiaries"
    beneficiary_id = Column(String(50),primary_key=True)
    pin= Column(String(4))
    imei= Column(String(50))
    intermediary_id = Column(String(50), ForeignKey("intermediaries.intermediary_id"))
    comment = relationship("Comment", backref=backref("beneficiaries", order_by="Comment.id"))
    
    def __init__(self,beneficiary_id,pin,imei,intermediary_id):
        self.beneficiary_id=beneficiary_id
        self.pin=pin
        self.imei=imei
        self.intermediary_id=intermediary_id 
        
    def setId(self):
        pass
    def setName(self):
        pass
    def setMobileNumber(self):
        pass
    def getId(self):
        pass
    def getName(self):
        pass
    def getMobileNumber(self):
        pass
    #def sendEncouregement(self):
    #    pass
    #def viewRewards(self):
    #    pass
    def __repr__(self):
        return str(self.beneficiary_id)

class Comment(Base):
    __tablename__="comments"
    id=Column(Integer, primary_key=True)
    commentdetails = Column(String(1000))
    date_captured = Column(Date)
    time_captured = Column(Time)
    message_sent_status= Column(Boolean)
    beneficiary_id = Column(String(50), ForeignKey("beneficiaries.beneficiary_id"))
    
    def __init__(self,beneficiary_id,commentsdetails,date_captured,time_captured,message_sent_status):
        self.beneficiary_id=beneficiary_id
        self.commentsdetails=commentsdetails
        self.date_captured=date_captured
        self.time_captured=time_captured
        self.message_sent_status=message_sent_status
     
    def setComment(self):
        pass
    def sendMessageWithComment(self):
        pass
    def __repr__(self):
        return str(self.commentdetails)
    
    
Base.metadata.create_all(db)


    
