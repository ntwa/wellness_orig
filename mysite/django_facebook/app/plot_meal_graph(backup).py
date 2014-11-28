#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, '..\\sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.food_beverage_module import FoodAndBeverage,Meal,MealComposition,db
from collections import OrderedDict


class switch(object):
          value = None
          def __new__(class_, value):
                    class_.value = value
                    return True
          
def case(*args):
          return any((arg == switch.value for arg in args))

class PlotMealGraph:
          def __init__(self,myjson):
                    self.myjson=myjson
          
          
          def getDataPoints(self):
                    errorcode={}
                    # Get data from fields
                    try:
                              
                              #day=self.myjson["Day"] 
                              #food_content=self.myjson["FoodContent"] 
                              #meal_type=self.myjson["MealType"]
                              #if day=="By date":
                              #     startdate=self.myjson["Date1"]
                              #     enddate=self.myjson["Date2"]
                              pass
                    
                    except Exception:
                              
                              errorcode["error"]=-1      
                              return (json.JSONEncoder().encode(errorcode))         
                         
                    beneficiary_id='KTLNTW00'
                    #food_content="Starch"
                    #meal_type="Lunch" 
                    day="Last week"
                    #startdate="2013-09-09"
                    #kunenddate="2013-09-15"
                    #print "Content-Type: text/html\n"
                    if day=="Today":
                              
                              startdate = datetime.date.today()
                              enddate = datetime.date.today()
                              
                    elif day=="This week":
                              
                              #from monday up to today's date. 
                              day_of_week = datetime.datetime.today().weekday()
                              enddate = datetime.date.today()
                              startdate = enddate-datetime.timedelta(day_of_week)
                              
                    elif day=="Last week":
                              day_of_week = datetime.datetime.today().weekday()
                              enddate = datetime.date.today()-datetime.timedelta(day_of_week+1)#last sunday
                              startdate = enddate-datetime.timedelta(6)# last monday
                    
                         
                    try:
                              
                              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                              engine=db
                              # create a Session
                              Session = sessionmaker(bind=engine)
                              
                              session = Session()
                              
                              
                              food_ids=[]
                              food_dates=[]
                              #food_ids={}
                              meals={}
                              meals_id=[]
                              key1="M" #for different meals
                              key2="P" #for different portion in the meals
                              key3="F" #for details attached in each portion. i.e. Date, food group, carbs group, portion size
                              first_posn=0
                              second_posn=0
                              third_posn=0
                              counter=0
                              meals_counter=0;
                              res = session.query(FoodAndBeverage).filter(FoodAndBeverage.beneficiary_id==beneficiary_id).filter(FoodAndBeverage.date_consumed>=startdate).filter(FoodAndBeverage.date_consumed<=enddate).order_by(FoodAndBeverage.date_consumed).all()
                              for food in res:
                                        
                                        food_ids.append(food.id)
                                        food_dates.append(food.date_consumed)
                                        print ("There is this food with ID= %s and it was eaten on %s")%(food.id,food.date_consumed)
                                   #food_ids[key+"%d"%pos]=food.id
                              
                              total_fruits_veg_sizes=0
                              total_starch_sizes=0
                              total_protein_sizes=0
                              total_fat_sizes=0
                              total_dairy_sizes=0
                              
                              
                              for fid in food_ids:
                                        
                                        #res2 = session.query(Meal,MealComposition).filter(Meal.food_id==fid).filter(Meal.meal_type==meal_type).filter(Meal.id==MealComposition.meal_id).filter(MealComposition.meal_group==food_content).all()
                                        res2 = session.query(Meal,MealComposition).filter(Meal.food_id==fid).filter(Meal.id==MealComposition.meal_id).all()
                                        meal_portion_tuples={}     
                                        if res2 is None:
                                             
                                                  pass
                                        else:
                                             
                                                  #meals[key+"%d"%pos]=(res2.id,res2.meal_type)
                                                  previous_id=None
                                                  meal_type=""
                                                  for m,c in res2:
                                                            meal_portion_tuple={}
                                                            if previous_id is None or previous_id is m.id:
                                                                      previous_id=m.id
                                                                      meal_type=m.meal_type
                                                            
                                                  
                                                  
                                                                      while switch(c.getMealGroup()):
                                                                 
                                                                                if case("Fruits and Vegetables"):
                                                                                          
                                                                                          total_fruits_veg_sizes=total_fruits_veg_sizes+c.getPortionSize()
                                                                                          #print "Fruits and Vegetables %s"%total_fruits_veg_sizes
                                                                                          break
                                                                                if case("Starch"):
                                                                                          total_starch_sizes=total_starch_sizes+c.getPortionSize()
                                                                                          #print "Starch. %s"%total_starch_sizes
                                                                                          break
                                                                                if case("Protein Foods"):
                                                                                          
                                                                                          total_protein_sizes=total_protein_sizes+c.getPortionSize()
                                                                                          #print "Protein Foods %s"%total_protein_sizes 
                                                                                          break
                                                                                if case("Fat Foods"):
                                                                                          
                                                                                          total_fat_sizes=total_fat_sizes+c.getPortionSize()
                                                                                          #print "Fat Foods. %s"%total_fat_sizes
                                                                                          break
                                                                                if case("Dairy"):
                              
                                                                                          total_dairy_sizes=total_dairy_sizes+c.getPortionSize()
                                                                                          #print "Dairy. %s"%total_dairy_sizes
                                                                                          break                                        
                                                                      
                                                                      meal_portion_tuple[key3+"%d"%third_posn]=food_dates[counter].strftime("%d/%m/%Y")
                                                                      third_posn=third_posn+1
                                                  
                                                                      meal_portion_tuple[key3+"%d"%third_posn]=c.getMealGroup()
                                                                      third_posn=third_posn+1
                                                  
                                                                      meal_portion_tuple[key3+"%d"%third_posn]=c.getCarbsGroup()
                                                                      third_posn=third_posn+1  
                                                  
                                                                      meal_portion_tuple[key3+"%d"%third_posn]=c.getPortionSize()
                                                                      third_posn=0                    
                                                                      meal_portion_tuples[key2+"%d"%second_posn]=meal_portion_tuple
                                                                      second_posn=second_posn+1                 
                                                                      '''                
                                                                           elif previous_id is m.id:
                                                                                meal_portion_tuple[key3+"%d"%third_posn]=c.getMealGroup()
                                                                                third_posn=third_posn+1
                                                                                
                                                                                meal_portion_tuple[key3+"%d"%third_posn]=c.getCarbsGroup()
                                                                                third_posn=third_posn+1  
                                                                                
                                                                                meal_portion_tuple[key3+"%d"%third_posn]=c.getPortionSize()
                                                                                third_posn=0                    
                                                                                meal_portion_tuples[key2+"%d"%second_posn]=meal_portion_tuple
                                                                                second_posn=second_posn+1                 
                                                                      '''    
                                                  
                                        
                                                  #print "-----The meal type on this one was %s"%meal_type                                                  
                                                  second_posn=0
                                                  is_not_empty = (meal_portion_tuples and True) or False
                                                  counter=counter+1
                                                  #print meal_portion_tuples
                                        
                                                  if is_not_empty:
                                                  
                                                            meals[key1+"%d"%first_posn]= meal_portion_tuples
                                                            first_posn=first_posn+1
                                        meals_counter=meals_counter+1
                                        
                              #total_no_of_portions=5;
                              #no_of_portions_iterated=0
                              portion_names=["Fruits and Vegetables","Starch","Protein Foods","Fat Foods","Dairy" ]
                              key1="P" #for different portions
                              key2="D" #for data in each portion                              
                              
                              first_posn=0
                              
                              
                              meal_portion_average_sizes={}# for storing all portions with their sizes
                              
                                                           
                              
                              
                              for food_portion_name in portion_names:
                                        
                                        second_posn=0
                                        meal_portion_average_size={} # for storing one portion with its size
                                        print food_portion_name
                                        '''
                                        while switch(food_portion_name):
                                                                                                        
                                                  if case("Fruits and Vegetables"):
                                                                                                                                 
                                                            meal_portion_average_size[key2+"%d"%second_posn]=food_portion_name
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=total_fruits_veg_sizes
                                                            second_posn=second_posn+1 
                                                            continue
                                                  
                                                  if case("Starch"):
                                                            
                                                            meal_portion_average_size[key2+"%d"%second_posn]=food_portion_name
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=total_starch_sizes
                                                            second_posn=second_posn+1                                                            
                                                            continue
                                                  
                                                  if case("Protein Foods"):
                                                            
                                                            meal_portion_average_size[key2+"%d"%second_posn]=food_portion_name
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=total_protein_sizes
                                                            second_posn=second_posn+1 
                                                            continue
                                                  
                                                  if case("Fat Foods"):
                                                            
                                                            meal_portion_average_size[key2+"%d"%second_posn]=food_portion_name
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=total_fat_sizes
                                                            second_posn=second_posn+1
                                                            continue
                                                  
                                                  if case("Dairy"):

                                                            meal_portion_average_size[key2+"%d"%second_posn]=food_portion_name
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=total_dairy_sizes
                                                            second_posn=second_posn+1
                                                            continue                                                  
                                        meal_portion_average_sizes[key1+"%d"%first_posn]=meal_portion_average_size
                                        first_posn=first_posn+1
                                        '''
                              
                              #print meal_portion_average_sizes
                              session.commit()
                              session.close()
                              return(json.JSONEncoder().encode(OrderedDict(sorted(meals.items(), key=lambda t: t[0]))))
                    except Exception as e:
                              errorcode["error"]=e     
                              return (json.JSONEncoder().encode(errorcode))                     
                    


obj=PlotMealGraph(1)
         
res=obj.getDataPoints()
print res