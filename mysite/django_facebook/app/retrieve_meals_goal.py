#!/usr/bin/env python
import datetime
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.health_goal_module import HealthGoal,MealGoal,db
import json

class RetrieveMealsGoal:
          def __init__(self,b_id):
                    self.b_id=b_id
             
          def getGoal(self):
                    try:
                              result_tuple={}
                              counter=0 
                              beneficiary_id=self.b_id  
                              engine=db 
                              # create a Session
                              Session = sessionmaker(bind=engine)
                              session = Session()
                              
                              res = session.query(HealthGoal).filter(HealthGoal.beneficiary_id==beneficiary_id).filter(HealthGoal.goaltype=="Meals").order_by(HealthGoal.datecaptured.desc()).first()
                              health_goal_id=res.id
                              # querying for a record in the physical_activity pattern table
                              #res = session.query(HealthGoal,MealGoal).filter(HealthGoal.id==MealGoal.health_goal_id).filter(HealthGoal.beneficiary_id==beneficiary_id).filter(HealthGoal.goaltype=="Meals").order_by(HealthGoal.datecaptured.desc()).all()
                              res = session.query(HealthGoal,MealGoal).filter(HealthGoal.id==MealGoal.health_goal_id).filter(HealthGoal.id==health_goal_id).filter(HealthGoal.beneficiary_id==beneficiary_id).filter(HealthGoal.goaltype=="Meals").all()
                                        
                              if res is None:
                                        result_tuple["Starch"]="None"
                                        result_tuple["Fruits"]="None"
                                        result_tuple["Fat"]="None"
                                        result_tuple["Protein"]="None"
                                        result_tuple["Dairy"]="None"
                                        #result_tuple["Duration"]="Weekly"                    
                              else:
                                                        
                                        for healthgoal,mealgoal in res:
                                                  if mealgoal.meal_group=="Starch":
                                                            starch=mealgoal.portion_size
                                                  elif mealgoal.meal_group=="Fruits and Vegetables":     
                                                            fruitsveg=mealgoal.portion_size
                                                  elif mealgoal.meal_group=="Fat Foods":
                                                            fat=mealgoal.portion_size
                                                  elif mealgoal.meal_group=="Protein Foods":
                                                            protein=mealgoal.portion_size
                                                  elif mealgoal.meal_group=="Dairy":
                                                            dairy=mealgoal.portion_size
                                                  #if counter == 0:
                                                  #          duration=healthgoal.duration
                                                  counter=counter+1                              
                                        
                                        result_tuple["Starch"]=starch
                                        result_tuple["Fruits"]=fruitsveg
                                        result_tuple["Fat"]=fat
                                        result_tuple["Protein"]=protein
                                        result_tuple["Dairy"]=dairy
                                        #result_tuple["Duration"]=duration
                                        #size=size-1 #ignore the last value because it has arleady been updated
                              #session.commit()
                              
                              
                    except Exception as e:
                              session.close()
                              engine.dispose() 
                              #print "Content-type: application/json"
                              result_tuple["Starch"]="None"
                              result_tuple["Fruits"]="None"
                              result_tuple["Fat"]="None"
                              result_tuple["Protein"]="None"
                              result_tuple["Dairy"]="None"           
                              #result_tuple["Duration"]=e
                              #sys.exit()
                     
                    #print "Content-type: application/json"
                    #print      
                    #print(json.JSONEncoder().encode(result_tuple))
                    session.close()
                    engine.dispose()
                    return json.JSONEncoder().encode(result_tuple)
          
#obj=RetrieveMealsGoal(8)
#goal=obj.getGoal()
#print goal