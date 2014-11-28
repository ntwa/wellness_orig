#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.food_beverage_module import FoodAndBeverage,Meal,MealComposition,db,dbconn
from collections import OrderedDict


class switch(object):
          value = None
          def __new__(class_, value):
                    class_.value = value
                    return True
def case(*args):
          return any((arg == switch.value for arg in args))
          

          

class PlotMealGraph:
          def __init__(self,myjson,b_id):
                    self.myjson=myjson
                    self.b_id=b_id
          
          def first_day_of_month(self,d):
                    return datetime.date(d.year, d.month, 1)
          
          def last_day_of_month(self,d):
                   
                    t=(calendar.monthrange(d.year,d.month))
                    return datetime.date(d.year,d.month,t[1])          

          def getDataPoints(self):
                    
                    # Get data from fields
                    try:
                              
                              day=self.myjson["Day"] 
                              #food_content=self.myjson["FoodContent"] 
                              #meal_type=self.myjson["MealType"]
                              #if day=="By date":
                              #     startdate=self.myjson["Date1"]
                              #     enddate=self.myjson["Date2"]
                              #pass
                    
                    except Exception:
                              
                              errorcode["error"]=-1      
                              return (json.JSONEncoder().encode(errorcode))         
                         
                    beneficiary_id=self.b_id
                    #food_content="Starch"
                    #meal_type="Lunch" 
                    #day="This week"
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
                              startdate = enddate-datetime.timedelta(days=day_of_week)
                                         
                    elif day=="Last week":
                              day_of_week = datetime.datetime.today().weekday()
                              enddate = datetime.date.today()-datetime.timedelta(days=(day_of_week+1))#last sunday
                              startdate = enddate-datetime.timedelta(days=6)# last monday


                    elif day=="This month":
                              #from 1st of this month to end of last month
                              startdate=self.first_day_of_month(datetime.date.today())
                              enddate=self.last_day_of_month(datetime.date.today())
                    
                         
                    elif day=="Last month":
                              #from 1st of last month to end of last month
                              #startdate=self.first_day_of_month(first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
                              startdate=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))               
                              enddate=self.last_day_of_month(startdate)
                              
                    
                    elif day=="Last three months":
                              # go two months back
                              first_day_last_month=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
                              startdate=self.first_day_of_month(first_day_last_month-datetime.timedelta(days=1))# subract 1 day to get to the end of a previous month before last month and get the first day of that month
                              enddate=self.last_day_of_month(datetime.date.today())#
                    else:
                              meals_tuples={}
                              meals_tuple={}
                    
                              key1="P"
                              key2="D"
                              first_posn=0
                              second_posn=0
                              meals_tuple[key2+"%d"%second_posn]="The system cannot recognize the period of time you have entered"
                              second_posn=second_posn+1
                                                                                                                                                                                            
                                                                                                                                                                                            
                              meals_tuple[key2+"%d"%second_posn]=-1
                              second_posn=0 
                              if first_posn<10:
                                   key1="P0"
                              else:
                                   key1="P"
                                                                                                                                                           
                              meals_tuples[key1+"%d"%first_posn]=meals_tuple
                                                                                                                                                         
                              first_posn=first_posn+1 
                              meals_tuple={}
                              return(json.JSONEncoder().encode(OrderedDict(sorted(meals_tuples.items(), key=lambda t: t[0]))))                             

                               
                       

                    
                    try:
                              
                              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                              engine=db
                              # create a Session
                              Session = sessionmaker(bind=engine)
                              
                              session = Session()
                              
                              
                              food_ids=[]
                              food_dates=[]
                              
                              meals={}
                              meals_id=[]
                              meals_counter=0.0# for counting the number of meals eaten
                              
                              
                              res = session.query(FoodAndBeverage).filter(FoodAndBeverage.beneficiary_id==beneficiary_id).filter(FoodAndBeverage.date_consumed>=startdate).filter(FoodAndBeverage.date_consumed<=enddate).order_by(FoodAndBeverage.date_consumed).all()
                              #get all the food_ids for the specified date range
                              for food in res:
          
                                        food_ids.append(food.id)
                                        food_dates.append(food.date_consumed)
                                        meals_counter=meals_counter+1.0
                              
                             
                              #print "Meals Counter%s"%meals_counter
                              
                              total_fruits_veg_sizes=0
                              total_starch_sizes=0
                              total_protein_sizes=0
                              total_fat_sizes=0
                              total_dairy_sizes=0
                              
                              if meals_counter == 0.0:
                                        meals_tuples={}
                                        meals_tuple={}
                              
                                        key1="P"
                                        key2="D"
                                        first_posn=0
                                        second_posn=0
                                        meals_tuple[key2+"%d"%second_posn]="No meals recorded in the specified period of time"
                                        second_posn=second_posn+1
                                                                                                                                                                                                      
                                                                                                                                                                                                      
                                        meals_tuple[key2+"%d"%second_posn]=-4
                                        second_posn=0 
                                        if first_posn<10:
                                             key1="P0"
                                        else:
                                             key1="P"
                                                                                                                                                                     
                                        meals_tuples[key1+"%d"%first_posn]=meals_tuple
                                                                                                                                                                   
                                        first_posn=first_posn+1 
                                        meals_tuple={}
                                        return(json.JSONEncoder().encode(OrderedDict(sorted(meals_tuples.items(), key=lambda t: t[0]))))                                          
                              
                             
                              for fid in food_ids:
                                        
                                        
                                        res2 = session.query(Meal,MealComposition).filter(Meal.food_id==fid).filter(Meal.id==MealComposition.meal_id).all()
                                        meal_portion_tuples={}     
                                        if res2 is None:
                                                  pass
                                        
                                        else:
                                                  
                                                  previous_id=None
                                                  meal_type=""
                                                  for m,c in res2:
                                                                                                                   
                                    
                                                  
                                                            if switch(c.getMealGroup()):
                                                                    
                                                                      if case("Fruits and Vegetables"):

                                                                                total_fruits_veg_sizes=total_fruits_veg_sizes+c.getPortionSize()
                                                                      
                                                                                continue
                                                                      if case("Starch"):
                                                                                
                                                                                total_starch_sizes=total_starch_sizes+c.getPortionSize()
                                                                                continue
                                                                      if case("Protein Foods"):
                                                                                
                                                                                total_protein_sizes=total_protein_sizes+c.getPortionSize()
                                                                                
                                                                                continue
                                                                      if case("Fat Foods"):
                                                                                
                                                                                total_fat_sizes=total_fat_sizes+c.getPortionSize()
                                                                                
                                                                                continue
                                                                      if case("Dairy"):
                                                                                
                                                                                total_dairy_sizes=total_dairy_sizes+c.getPortionSize()
                                                                                
                                                                                continue 
                                                                      
                                                                                                              
                                                  
                                 
                                        
                              
                              portion_names=["Fruits and Vegetables","Starch","Protein Foods","Fat Foods","Dairy" ]
                              key1="P" #for different portions
                              key2="D" #for data in each portion                              
                              
                              first_posn=0
                              
                              
                              meal_portion_average_sizes={}# for storing all portions with their sizes
                              
                                                           
                              
                              
                              if meals_counter>0.0:
                                        # get the sum of each portion and compute the average. The avrage is computed using the sum of portion sizes of a different food group divided by the total number of meals
                                        for food_portion_name in portion_names:
                                                 
                                                  second_posn=0
                                                  meal_portion_average_size={} # for storing one portion with its size
                                                  
                                                  
                                                                                                                  
                                                  if food_portion_name=="Fruits and Vegetables":
                                                            
                                                                                                                                           
                                                            meal_portion_average_size[key2+"%d"%second_posn]="Fruits & Veg"
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=float("{0:.2f}".format(total_fruits_veg_sizes/meals_counter))
                                                            second_posn=second_posn+1 
                                                                      
                                                            
                                                  elif food_portion_name=="Starch":
                                                                     
                                                            meal_portion_average_size[key2+"%d"%second_posn]="Starch"
                                                            second_posn=second_posn+1
                                                            print total_starch_sizes
                                                            meal_portion_average_size[key2+"%d"%second_posn]=float("{0:.2f}".format(total_starch_sizes/meals_counter))
                                                            second_posn=second_posn+1                                                            
                                                  
                                                            
                                                  elif food_portion_name=="Protein Foods":
                                                                      
                                                            meal_portion_average_size[key2+"%d"%second_posn]="Protein"
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=float("{0:.2f}".format(total_protein_sizes/meals_counter))
                                                            second_posn=second_posn+1 
                                                            
                                                           
                                                  if food_portion_name=="Fat Foods":
                                                                      
                                                            meal_portion_average_size[key2+"%d"%second_posn]="Fat"
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=float("{0:.2f}".format(total_fat_sizes/meals_counter))
                                                            second_posn=second_posn+1
                                                  
                                                            
                                                  if food_portion_name=="Dairy":
          
                                                            meal_portion_average_size[key2+"%d"%second_posn]="Dairy"
                                                            second_posn=second_posn+1
                                                            meal_portion_average_size[key2+"%d"%second_posn]=float("{0:.2f}".format(total_dairy_sizes/meals_counter))
                                                            second_posn=second_posn+1
                                                  if first_posn<10:
                                                                
                                                            key1="P0"
                                                  else:
                                                            key1="P"                                                  
                                                                                                              
                                                  meal_portion_average_sizes[key1+"%d"%first_posn]=meal_portion_average_size
                                                  first_posn=first_posn+1
                                        
                            
                              session.close()
                              engine.dispose()
                              dbconn.close()

                              return(json.JSONEncoder().encode(OrderedDict(sorted(meal_portion_average_sizes.items(), key=lambda t: t[0]))))
                    except Exception as e:
                              session.close()
                              engine.dispose()
                              dbconn.close()
               
                              key1="P" #for different portions
                              key2="D" #for data in each portion 
                              second_posn=0 
                              meal_portion_average_size={}
    
                              meal_portion_average_size[key2+"%d"%second_posn]="%s"%e
                              second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
                              meal_portion_average_size[key2+"%d"%second_posn]=-1
                              second_posn=0 
                              if first_posn<10:
                                  
                                  key1="P0"
                              else:
                                  key1="P"
                                                                                                                                            
                              meal_portion_average_sizes[key1+"%d"%first_posn]=meal_portion_average_size
                                                                                                                                          
                              first_posn=first_posn+1 
                              meal_portion_average_size={}
                              return(json.JSONEncoder().encode( meal_portion_average_sizes))                    
                    

#myjson={"Day":"Last three months"}
#obj=PlotMealGraph(myjson,8)
         
#res=obj.getDataPoints()
#print res
