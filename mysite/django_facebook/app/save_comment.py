#!/usr/bin/env python
import datetime,time,calendar
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.intermediary_module import Intermediary,Beneficiary,Comment,db,dbconn


class SaveComment:
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id

     def first_day_of_month(self,d):
          return datetime.date(d.year, d.month, 1)
      
     def last_day_of_month(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return datetime.date(d.year,d.month,t[1])


     def saveCommentInDB(self):
          
          commentdetails="" 
          date_captured="" 
          time_captured="" 
          event_start_date=""
          event_end_date=""
          event_type=""
          message_sent_status=""
          result={}
          allow_insert=1
          
          # Get data from fields
          try:
                            
               commentdetails=self.myjson["MessageBody"] 
               date_captured=datetime.date.today()# today's date
               time_captured=time.strftime("%H:%M:%S")
               day=self.myjson["Day"]
               #event_start_date=self.myjson["StartDate"] 
               #event_end_date=self.myjson["EndDate"] 
               event_type=self.myjson["EventType"]
               message_sent_status=False          
               

               
                
          except Exception:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object'
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if (commentdetails=="None") and (day=="None") and (event_type=="None"):
               #print "Content-type: text/html\n" 
               result["message"]="There is an error in saving your message due to missing of some information"
               return (json.JSONEncoder().encode(result)) 
               #sys.exit()

               #sys.exit()



          if day=="Today":
               event_start_date = datetime.date.today()
               event_end_date = datetime.date.today()             
               
          elif day=="This week":
               #from monday up to sunday. 
               day_of_week = datetime.datetime.today().weekday()
               event_start_date =datetime.date.today()-datetime.timedelta(days=day_of_week)#monday
               event_end_date=event_start_date+datetime.timedelta(days=6)#sunday
     
              
          elif day=="Last week":
               day_of_week = datetime.datetime.today().weekday()
               event_end_date = datetime.date.today()-datetime.timedelta(days=(day_of_week+1))#last sunday. Subtract today from the number of days that have passed since sunday
               event_start_date  = event_end_date-datetime.timedelta(days=6)# Monday of the previous week.            
               
          elif day=="This month":
               #from 1st of this month to end of last month
               event_start_date =self.first_day_of_month(datetime.date.today())
               event_end_date=self.last_day_of_month(datetime.date.today())
          
               
          elif day=="Last month":
               #from 1st of last month to end of last month
               #startdate=self.first_day_of_month(first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
               event_start_date =self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))               
               event_end_date=self.last_day_of_month(event_start_date)
          
          elif day=="Last three months":
               # go two months back
               first_day_last_month=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
               event_start_date =self.first_day_of_month(first_day_last_month-datetime.timedelta(days=1))# subract 1 day to get to the end of a previous month before last month and get the first day of that month
               event_end_date=self.last_day_of_month(datetime.date.today())#
          else:
               result["message"]="Error: Failed to save a message."
               return (json.JSONEncoder().encode(result))              


               
          
          if allow_insert==1:           
               try:
                    
                    #print "Content-Type: text/html\n"
                    #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                    engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
                    
                    session = Session()
                    
                    # Create food
                    #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                    
                    new_comment=Comment(self.b_id,commentdetails,date_captured,time_captured,event_start_date,event_end_date,event_type,message_sent_status)
                                            
                    
                    
                    session.add(new_comment)
                    
                    
                    # commit the record the database
                    
                    
                    session.commit()
                    session.close()
                    engine.dispose()
                    dbconn.close()                 
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    dbconn.close()

                    result["message"]=e
                    return (json.JSONEncoder().encode(result)) 
               
               result["message"]="The message was saved successfully. It will be delivered  later."
               return (json.JSONEncoder().encode(result))
     
     
#myjson={"MessageBody":"Hi mom. You have reached your activity goal this week. Keep it up!!","Day":"This month","EventType":"Meal"}


#obj=SaveComment(myjson,8)
#msg=obj.saveCommentInDB()
#print msg
