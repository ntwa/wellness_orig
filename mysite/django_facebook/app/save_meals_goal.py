#!/usr/bin/env python
import datetime
import sys
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.health_goal_module import HealthGoal,MealGoal,db
import json

class SaveMealsGoal:
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id
          
     def saveGoal(self):
     
          
          allow_insert=1
          #print "Content-type: application/json"
          # Get data from fields
          result={}
          try:
               starch=self.myjson["Starch"] 
               fruitsveg=self.myjson["Fruits"] 
               dairy=self.myjson["Dairy"] 
               fat=self.myjson["Fat"] 
               protein=self.myjson["Protein"] 
               #duration=self.myjson["Duration"]
               #starch="Large" 
               #fruitsveg="None"
               #dairy="None" 
               #fat="Medium"
               #protein="Small"  
               #duration="Monthly"
          except Exception:
               #print "Content-type: text/html\n" 
               #print "Content-type: application/json"
               result["message"]='There was an error in processing a JSON object'
               #print      
               return (json.JSONEncoder().encode(result))     
               #sys.exit() 
          
          
               
          date_captured = datetime.date.today() 
          
          if(starch=="None") and (fruitsveg=="None") and (dairy=="None") and (fat=="None") and (protein=="None"):   
               result["message"]='Error: You have not specified any portion size in your meal goal'
               #print      
               return (json.JSONEncoder().encode(result))     
               #sys.exit()      
          
          
          #print "Content-Type: text/html\n"
          counter=0
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                    
               # querying for a record in the physical_activity pattern table
               res= session.query(HealthGoal,MealGoal).filter(HealthGoal.id==MealGoal.health_goal_id).filter(HealthGoal.beneficiary_id==self.b_id).filter(HealthGoal.datecaptured==date_captured).filter(HealthGoal.goaltype=="Meals").all()
               if res is None:
                         pass
               else:
                    for healthgoal,mealgoal in res:
                         if mealgoal.meal_group=="Starch":
                              mealgoal.portion_size=starch
                         elif mealgoal.meal_group=="Fruits and Vegetables":     
                              mealgoal.portion_size=fruitsveg
                         elif mealgoal.meal_group=="Fat Foods":
                              mealgoal.portion_size=fat
                         elif mealgoal.meal_group=="Protein Foods":
                              mealgoal.portion_size=protein
                         elif mealgoal.meal_group=="Dairy":
                              mealgoal.portion_size=dairy
                         #if counter == 0:
                         #     healthgoal.duration=duration
                         counter=counter+1
                    
                              
                         allow_insert=0
                         #size=size-1 #ignore the last value because it has arleady been updated
                         session.commit()
                         result["message"]="The goal was updated successfully"
                    
                    
          except Exception as e:
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()     
               result["message"]=e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
          
          
          
          
          
          if allow_insert==1:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
               # create a Session
               #Session = sessionmaker(bind=engine)
          
               #session = Session()
               
               
               
               # Create food
               #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
               try:
                   
                  new_health_goal=HealthGoal(self.b_id,date_captured,"Meals")
                  meal_portions=[MealGoal("High Carbs",starch,"Starch"),MealGoal("Low Carbs",fruitsveg,"Fruits and Vegetables"),MealGoal("Low Carbs",fat,"Fat Foods"),MealGoal("Low Carbs",protein,"Protein Foods"),MealGoal("Low Carbs",dairy,"Dairy")]
               
                  new_health_goal.meals_goal=[]
                  new_health_goal.meals_goal.extend(meal_portions)
                   
               
               
               # Add the record to the session object
               
               
                  session.add(new_health_goal)
               
               
               # commit the record the database
               
               
                  session.commit()
                  result["message"]="The goal was set successfully" 
               except Exception as e:
                  result["message"]="Failed to save this meal due to the following error: %s"%e.message
                  pass   
               
           

          session.close()
          engine.dispose()
          #print      
          return (json.JSONEncoder().encode(result))