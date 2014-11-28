#!C:/Python27/python.exe
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.activity_module import PhysicalActivity,db
from wellness.applogic.intermediary_module import Beneficiary
import sys, json

myjson = json.load(sys.stdin)

modify=1
counter=0


# Get data from fields
class SyncActivityModule:
     
     def __init__(self,myjson):
          self.myjson=myjson
          
     def uploadActivity(self):     
          try:
               stepsarray=self.myjson["header"]["steps"]
               datecapturedarray=self.myjson["header"]["datecaptured"]
               starthrarray=self.myjson["header"]["starthr"]
               endhrarray=self.myjson["header"]["endhr"]
               size=self.myjson["header"]["length"]  
               IMEI=self.myjson["header"]["IMEI"]
               
               
               #stepsarray=[200,140]
               #datecapturedarray=['2013-10-09','2013-10-10']
               #starthrarray=['12:00','13:00']
               #endhrarray=['12:59','13:59']
               #size=2             
          except Exception as e:
               #print "Content-type: text/html\n" 
               #print('There was an error in processing a JSON object')
               #print e
               sys.exit() 
     
          #print "Content-Type: text/html\n"
     
          #get beneficiary_id through supplied IMEI
     
     
          try:
               engine=db 
              
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               
               # querying for a record in the physical_activity pattern table
               res = session.query(Beneficiary).filter(Beneficiary.imei==IMEI).first()
               if res is None:
                         beneficiary_id=None
               else:
                         beneficiary_id=res.beneficiary_id
                         
                         session.commit()
                             
                    
                    
                    
          except Exception as e:
               #print "Content-type: text/html\n" 
               #print('There was an error')
               #print e
               sys.exit()
          
          
          
          
          
          
          
          
          #first check if the last record arleady exists in the database and tryi to update. Possibly this record is currently in use by the pedoemeter
          
          try:
                    engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                    for i in range(size):
                              # create a Session
                              Session = sessionmaker(bind=engine)
                              session = Session()
                    
                              # querying for a record in the physical_activity pattern table
                              res = session.query(PhysicalActivity).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured==datecapturedarray[i]).filter(PhysicalActivity.starttimecaptured==starthrarray[i]).first()
                              if res is None:
                                        continue
                              else:
                                        res.stepscounter=stepsarray[i]
                                        #size=size-1 #ignore the last value because it has arleady been updated
                                        session.commit()
                                        #pop a record so that it doesn't get inserted 
                                        stepsarray.pop(i)
                                        datecapturedarray.pop(i)
                                        starthrarray.pop(i)
                                        endhrarray.pop(i)
                                        counter=counter+1
                    
                    
                    
          except Exception as e:
                    print "Content-type: text/html\n" 
                    print('There was an error')
                    print e
                    sys.exit()           
          #needs to be edited
          size=size-counter
          if modify == 1:
                    try:
                              engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                              for i in range(size):
                                        # create a Session
                                        Session = sessionmaker(bind=engine)
                    
                                        session = Session()
                                        # Create Activity Pattern
                                        #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                                        new_activity_pattern=PhysicalActivity(beneficiary_id,datecapturedarray[i],starthrarray[i],endhrarray[i],stepsarray[i])
                    
                    
                    
                    
                                        # Add the record to the session object
                    
                    
                                        session.add(new_activity_pattern)
                    
                    
                                        # commit the record the database
                    
                    
                                        session.commit()
                     
                    except Exception as e:
                              print "Content-type: text/html\n" 
                              print('There was an error')
                              print e
                              sys.exit()           
                    
          print "STEP_SYNC_SUCCESS"