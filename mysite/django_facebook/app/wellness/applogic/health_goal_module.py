from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool
#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()
       
class HealthGoal(Base):
    __tablename__="health_goals"
    id=Column(Integer, primary_key=True)
    beneficiary_id = Column(Integer)
    datecaptured = Column(Date,nullable=False)
    #duration=Column(String(50))
    goaltype=Column(Enum('Activity','Meals'),nullable=False)
    activitygoal = relationship("ActivityGoal", backref=backref("health_goal", order_by=id))
    meals_goal = relationship("MealGoal", backref=backref("health_goal", order_by=id))
    def __init__(self,beneficiary_id,datecaptured,goaltype):
        self.datecaptured=datecaptured
        self.beneficiary_id=beneficiary_id
        self.goaltype=goaltype
    @abstractmethod    
    def setGoal(self):
        pass
    @abstractmethod
    def viewGoal(self):
        pass

    def __repr__(self):
        return str(self.beneficiary_id)


class ActivityGoal(Base):     
    __tablename__="activitygoals"
    id=Column(Integer, primary_key=True)
    steps=Column(Integer)
    health_goal_id = Column(Integer, ForeignKey("health_goals.id"))
        
    def __init__(self,steps):
        self.steps=steps
    def __repr__(self):
        return str(self.steps)    


class MealGoal(Base):     
    __tablename__="meals_goal"
    id=Column(Integer, primary_key=True)
    carbs_group=Column(String(20))
    portion_size=Column(String(20))
    meal_group=Column(String(50))  
    health_goal_id = Column(Integer, ForeignKey("health_goals.id"))
    def __init__(self,carbs_group,portion_size,meal_group):
        self.carbs_group=carbs_group
        self.portion_size=portion_size
        self.meal_group=meal_group    
    def setCarbsGroup(self):
        pass
    def setPortionSize(self):
        pass;
    def setFoodGroup(self):
        pass;
    def getCarbsGroup(self):
        return self.carbs_group
    def getPortionSize(self):
        return self.portion_size
    def getMealGroup(self):
        return self.meal_group    


Base.metadata.create_all(db)
