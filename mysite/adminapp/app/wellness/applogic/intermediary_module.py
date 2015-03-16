from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Time, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr


db = create_engine(connstr ,pool_size=20, max_overflow=0)
Base = declarative_base()

       
class Intermediary(Base):
    __tablename__="intermediaries"
    intermediary_id = Column(String(50),primary_key=True)
    intermediary_fname=Column(String(50))
    intermediary_lname=Column(String(50))
    mobile=Column(String(50))    
    #passwd= Column(String(50))
    beneficiary = relationship("Beneficiary", backref=backref("intermediaries", order_by=intermediary_id))
    #beneficiary = relationship("Beneficiary",uselist=False, backref="intermediaries")
    def __init__(self,intermediary_id,intermediary_fname,intermediary_lname,mobile):
        self.intermediary_id=intermediary_id
        self.intermediary_fname=intermediary_fname
        self.intermediary_lname=intermediary_lname
        self.mobile=mobile
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
    #def __repr__(self):
    #    return str("%s %s. UserID:%s"%(self.intermediary_fname,self.intermediary_lname,self.intermediary_id))
       
class Beneficiary(Base):
    __tablename__="beneficiaries"
    id = Column(Integer,primary_key=True)
    beneficiary_fname=Column(String(50))
    beneficiary_lname=Column(String(50))
    beneficiary_mobile=Column(String(20))
    relation=Column(String(50))
    team_name=Column(String(30))
    gender=Column(String(10))
    intermediary_id = Column(String(50), ForeignKey("intermediaries.intermediary_id"))
    comment = relationship("Comment", backref=backref("beneficiaries", order_by="Comment.id"))
    
    def __init__(self,beneficiary_fname,beneficiary_lname,beneficiary_mobile,intermediary_id,relation,team_name,gender):     

        self.beneficiary_fname=beneficiary_fname
        self.beneficiary_lname=beneficiary_lname
        self.beneficiary_mobile=beneficiary_mobile
        self.intermediary_id=intermediary_id 
        self.relation=relation
        self.team_name=team_name
        self.gender=gender      
         
    def setId(self):
        pass
    def getBeneficiaryId(self):
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
    #def __repr__(self):
    #    return str(self.beneficiary_id)

class Comment(Base):
    __tablename__="comments"
    id=Column(Integer, primary_key=True)
    commentdetails = Column(String(500),nullable=False)
    date_captured = Column(Date,nullable=False)
    time_captured = Column(Time,nullable=False)
    event_start_date=Column(Date,nullable=False)
    event_end_date=Column(Date,nullable=False)
    event_type=Column(Enum('Activity','Meal','Weight'), nullable=False)
    message_sent_status= Column(Boolean)
    beneficiary_id = Column(Integer, ForeignKey("beneficiaries.id"))
    
    def __init__(self,beneficiary_id,commentdetails,date_captured,time_captured,event_start_date,event_end_date,event_type,message_sent_status):
        
        self.beneficiary_id=beneficiary_id
        self.commentdetails=commentdetails
        self.date_captured=date_captured
        self.time_captured=time_captured
        self.event_start_date=event_start_date
        self.event_end_date=event_end_date
        self.event_type=event_type
        self.message_sent_status=message_sent_status
        
     
    def setComment(self):
        pass
    def sendMessageWithComment(self):
        pass
    def __repr__(self):
        return str(self.commentdetails)
    
    
Base.metadata.create_all(db)


    
