#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.food_beverage_module import FoodAndBeverage,Meal,MealComposition,db,dbconn


class SaveMeal:
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id
     def saveMealInDB(self):
          
          starch="" 
          fruitsveg="" 
          dairy="" 
          fat=""
          protein="" 
          result={}
          allow_insert=1
          
          # Get data from fields
          try:
                            
               starch=self.myjson["Starch"] 
               fruitsveg=self.myjson["Fruits"] 
               dairy=self.myjson["Dairy"] 
               fat=self.myjson["Fat"] 
               protein=self.myjson["Protein"] 
               date_eaten=self.myjson["DateEaten"]
               meal_type=self.myjson["MealType"]          
               
               
               '''
               starch="Medium"
               fruitsveg="None"
               dairy="Large" 
               fat="None"
               protein="None" 
               date_eaten="2013-02-23"
               meal_type="Lunch"
               '''
               
                
          except Exception:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object'
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if(starch=="None") and (fruitsveg=="None") and (dairy=="None") and (fat=="None") and (protein=="None"):
               #print "Content-type: text/html\n" 
               result["message"]="Error: You have not specified any portion size in your meal"
               return (json.JSONEncoder().encode(result)) 
               #sys.exit()


          #check if a meal type exists
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(FoodAndBeverage,Meal).filter(FoodAndBeverage.id==Meal.food_id).filter(FoodAndBeverage.date_consumed==date_eaten).filter(FoodAndBeverage.beneficiary_id==self.b_id).first()
               if res is None:
                    session.close()
                    engine.dispose()
                    dbconn.close()
               else:
                    food_record,meal_record=res
                    meal_record_id=meal_record.id
                    res= session.query(MealComposition).filter(MealComposition.meal_id==meal_record_id).all()
                    for portion_tuple in res:
                         
                         if( portion_tuple.meal_group== "Starch") :
                              portion_tuple.portion_size=starch;
                         elif portion_tuple.meal_group== "Fruits and Vegetables" :
                              portion_tuple.portion_size=fruitsveg
                         elif portion_tuple.meal_group== "Fat" :
                              portion_tuple.portion_size=fat
                         elif portion_tuple.meal_group== "Dairy" :
                              portion_tuple.portion_size=dairy
                         elif portion_tuple.meal_group== "Protein" :
                              portion_tuple.portion_size=protein
                                
                                             
                    allow_insert=0
                    #size=size-1 #ignore the last value because it has arleady been updated
                    session.commit()
                    result["message"]="The following meal %s that was eaten on this date %s already existed in the database and it was updated"%(meal_type,date_eaten)
                    session.close()  
                    engine.dispose()   
                    dbconn.close()

                    return (json.JSONEncoder().encode(result))     
                                   
          except Exception as e:
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          
          if allow_insert==1:           
               try:
                    
                    #print "Content-Type: text/html\n"
                    #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                    #engine=db
                    # create a Session
                    #Session = sessionmaker(bind=engine)
                    
                    #session = Session()
                    
                    # Create food
                    #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                    new_food=FoodAndBeverage(self.b_id,date_eaten)
                    new_meal=Meal(meal_type)
                    meal_portions=[MealComposition("High Carbs",starch,"Starch"),MealComposition("Low Carbs",fruitsveg,"Fruits and Vegetables"),MealComposition("Low Carbs",fat,"Fat Foods"),MealComposition("Low Carbs",protein,"Protein Foods"),MealComposition("Low Carbs",dairy,"Dairy")]
                    #meal_portions=[MealComposition("High Carbs",starch,"Starch"),MealComposition("Low Carbs",fat,"Fat Foods")]#,MealComposition("Low Carbs",protein,"Protein Foods"),MealComposition("Low Carbs",dairy,"Dairy")]
                    
                    new_meal.meal_composition=[]
                    new_meal.meal_composition.extend(meal_portions)
                    new_food.meal=[new_meal]
                   
                    #result["message"]="%s%s%s%s%s"%(starch,fruitsveg,fat,dairy,protein)
                    #return (json.JSONEncoder().encode(result))                                               
                                 
                    
                    
                    session.add(new_food)
                    
                    
                    # commit the record the database
                    
                    
                    session.commit()
      
                                     
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    result["R00"]={"F1":-6,"F0":e.message}
                    dbconn.close()
                    return (json.JSONEncoder().encode(result)) 
               session.close()
               engine.dispose()
               dbconn.close()

               result["R00"]={"F1":1,"F0":"The meal was recorded sucessfully"}
               return (json.JSONEncoder().encode(result))
     
     
#myjson={"Starch":"Medium","Fruits":"None","Fat":"Small","Dairy":"None","Protein":"Small","DateEaten":"2014-08-22","MealType":"Lunch"}


#obj=SaveMeal(myjson,8)
#msg=obj.saveMealInDB()
#print msg
