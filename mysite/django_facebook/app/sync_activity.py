#!/usr/bin/env python
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.activity_module import PhysicalActivity,db,dbconn
#from wellness.applogic.intermediary_module import Beneficiary
from wellness.applogic.intermediary_module import Intermediary,Beneficiary,Comment
import sys, json
from threading import Lock





# Get data from fields
class SyncActivityModule():
     lock = Lock()
     
     def __init__(self,myjson):
          self.myjson=myjson
                   
          
     def uploadActivity(self):
          
          self.lock.acquire()          
          self.modify=1
          self.counter=0 
          result={}
          try:
               stepsarray=self.myjson["header"]["steps"]
               datecapturedarray=self.myjson["header"]["datecaptured"]
               starthrarray=self.myjson["header"]["starthr"]
               endhrarray=self.myjson["header"]["endhr"]
               size=self.myjson["header"]["length"]  
               IMEI=self.myjson["header"]["Intermediary"]
               
               
               
               
               #stepsarray=[400,600]
               #datecapturedarray=['2014-11-14','2012-08-24']
               #starthrarray=['12:00','13:00']
               #endhrarray=['12:59','13:59']
               #size=2 
               #IMEI="katulentwa@gmail.com"
          except Exception as e:
               #print "Content-type: text/html\n" 
               #print('There was an error in processing a JSON object')
               result["message"]=e
               return json.JSONEncoder().encode(result)
          
          #self.lock.release()          
          #print "Content-Type: text/html\n"
     
          #get beneficiary_id through supplied IMEI
          
          
          #result["message"]={}
          #result["message"]=stepsarray[0]
          #return json.JSONEncoder().encode(result)
     
          
          
          try:
               engine=db 
              
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               
               # querying for a record in the physical_activity pattern table
               res = session.query(Beneficiary).filter(Beneficiary.intermediary_id==IMEI).first()
               
               if res is None:
                         beneficiary_id=None
               else:
                         beneficiary_id=res.id
                         
                         session.commit()
                             
                    
               session.close()     
                    
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]=e
               #return json.JSONEncoder().encode(result)
          
          
          
          
          #first check if the last record arleady exists in the database and trying to update. Possibly this record is currently in use by the pedoemeter
          i=0
          element_pop=0
          try:
                    #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                    for i in range(size):
                    #while size>=i:

                         # create a Session
                         #Session = sessionmaker(bind=engine)
                         #session = Session()
                         
                         if element_pop >= 1:
                              i=i-element_pop
                         
                         # querying for a record in the physical_activity pattern table
                         res = session.query(PhysicalActivity).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured==datecapturedarray[i]).filter(PhysicalActivity.starttimecaptured==starthrarray[i]).first()

                         
                         if res is None:
                                   continue
                         else:     

                                  
                                   res.stepscounter=stepsarray[i]
                                   session.commit()
                                   #size=size-1 #ignore the last value because it has arleady been updated
                                 
                                   #pop a record so that it doesn't get inserted 
                                   
                                   stepsarray.pop(i)
                                   datecapturedarray.pop(i)
                                   starthrarray.pop(i)
                                   endhrarray.pop(i)
                                   self.counter=self.counter+1
                                   
                                   element_pop=element_pop+1
                      
                                   #session.commit()
                    #result["message"]={}
                    #result["message"]=stepsarray[0]
                    #return json.JSONEncoder().encode(result)                    
          except Exception as e:
               result["message"]=e
               session.close()
               engine.dispose()
               dbconn.close()
               self.lock.release()
               return json.JSONEncoder().encode(result)          
          #needs to be edited
          size=size-self.counter
          
          if self.modify == 1:
               
               try:      
                         min_date_allowed='2014-01-01'
                         orig_min_date=datetime.datetime.strptime(min_date_allowed , '%Y-%m-%d').date()
                         #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                         engine=db
                         for i in range(size):
                                   # create a Session
                                   Session = sessionmaker(bind=engine)
               
                                   session = Session()
                                   # Create Activity Pattern
                                   #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                                   #new_activity_pattern=PhysicalActivity(beneficiary_id,datecapturedarray[i],starthrarray[i],endhrarray[i],stepsarray[i])
               
                                   datecaptured=datecapturedarray[i]
                                   orig_date=datetime.datetime.strptime(datecaptured , '%Y-%m-%d').date()

                                  
                                   if  orig_date<orig_min_date:
                                        print "rejected"
                                   else:
                                        new_activity_pattern=PhysicalActivity(beneficiary_id,datecapturedarray[i],starthrarray[i],endhrarray[i],stepsarray[i])
               
                                        # Add the record to the session object
               
               
                                        session.add(new_activity_pattern)
               
               
                                        # commit the record the database
               
               
                                        session.commit()
                
               except Exception as e:
                    session.close()
                    engine.dispose()
                    dbconn.close()
                    result["message"]=e
                    self.lock.release()
                    return json.JSONEncoder().encode(result)         
                    
          session.close()
          engine.dispose()
          result["message"]="STEP_SYNC_SUCCESS"
          self.lock.release()
          return json.JSONEncoder().encode(result)          

#myjson={"header":{"steps":[200,140]}}
#myjson={"header":{"datecaptured":{0:'2013-10-05',1:'2013-10-07'}}}
#myjson={"header":{"starthr":{0:'12:00',1:'13:00'}}}
#myjson={"header":{"endhr":{0:'12:59',1:'13:59'}}}
#myjson={"header":{"length":2}}
#myjson={"header":{"IMEI":"katulentwa@gmail.com"}}
          
#obj=SyncActivityModule(myjson);
#print obj.uploadActivity()
