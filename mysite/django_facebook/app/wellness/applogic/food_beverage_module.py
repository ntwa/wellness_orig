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

Base = declarative_base()

       
class FoodAndBeverage(Base):
    __tablename__="food_beverage"
    id=Column(Integer, primary_key=True)
    beneficiary_id = Column(Integer)
    date_consumed = Column(Date)
    meal = relationship("Meal", backref=backref("food_beverage", order_by=id))
    def __init__(self,beneficiary_id,date_consumed):
        self.date_consumed=date_consumed
        self.beneficiary_id=beneficiary_id
    @abstractmethod    
    def storeFoodAndBevarageConsumption(self):
        pass
    @abstractmethod
    def viewFoodAndBeverageConsumption(self):
        pass
    @abstractmethod
    def drawChart(self):
        pass
    #def __repr__(self):
    #    return str(self.beneficiary_id)



class Meal(Base):     
    __tablename__="meals"
    id=Column(Integer, primary_key=True)
    meal_type=Column(String(50))
    food_id = Column(Integer, ForeignKey("food_beverage.id"))
    meal_composition = relationship("MealComposition", backref=backref("meals", order_by=id))
    
    def __init__(self,meal_type):
        self.meal_type=meal_type
    #def __repr__(self):
    #    return str(self.meal_type)    

class MealComposition(Base):
    __tablename__="meal_composition"
    id=Column(Integer, primary_key=True)
    carbs_group=Column(String(20))
    portion_size=Column(String(20))
    meal_group=Column(String(50))  
    meal_id = Column(Integer, ForeignKey("meals.id"))
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
        if self.portion_size=="Large":
            return 3
        elif self.portion_size=="Medium":
            return 2
        elif self.portion_size=="Small":
            return 1
        else:
            return 0
        
        return self.portion_size
    def getMealGroup(self):
        return self.meal_group



Base.metadata.create_all(db)
