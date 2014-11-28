#!/usr/bin/env python
import datetime
import time
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.logs_module import Logs,db,dbconn
from collections import OrderedDict


class SaveLogs:
     def __init__(self,myjson,intermediary_id):
          self.myjson=myjson
          self.intermediary_id=intermediary_id
     def saveLogsInDB(self):
               
          datecaptured=""
          timecaptured=""
          clickscounter=0
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               clickscounter=self.myjson["ClicksCounter"]; 
               #clickscounter=40
               datecaptured = datetime.date.today()
               #timecaptured=time.strftime("%H:%M:%S")
               timecaptured=time.strftime("%H:%M:%S")
               
               e="Error"
                        
                             
          except Exception as e:
               logs_tuples={}
               logs_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               logs_tuple[key2+"%d"%second_posn]=e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               logs_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               logs_tuples[key1+"%d"%first_posn]=logs_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               logs_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(logs_tuples.items(), key=lambda t: t[0]))))
          


               
          
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(Logs).filter(Logs.intermediary_id==self.intermediary_id).filter(Logs.datecaptured==datecaptured).filter(Logs.timecaptured==timecaptured).first()
               if res is None:
                    pass
               else:
                    logsrecord=res
                    previousclickscounter=logsrecord.clickscounter
                    logsrecord.clickscounter=previousclickscounter+clickscounter#increment existing click counter
                                
                                             
                    allow_insert=0
                    
                    session.commit()
                    result["message"]="The log record for this date existed and it was updated from %s clicks to %s clicks"%(previousclickscounter,(clickscounter+previousclickscounter))
                               
                                   
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
                    #engine=db
                    # create a Session
                    #Session = sessionmaker(bind=engine)
               
                    #session = Session()
               
                    # Create weight
                    #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                    new_clickscounter=Logs(self.intermediary_id,clickscounter,datecaptured,timecaptured)
                         
                    session.add(new_clickscounter)
               
               
                    # commit the record the database
               
               
                    session.commit()
                    result["message"]="The clicks was recorded sucessfully"
                    
               except Exception as e:
                    result["message"]=e
                    session.close()
                    engine.dispose()
                    dbconn.close()

                    return (json.JSONEncoder().encode(result)) 
          
          session.close()
          engine.dispose()          
          dbconn.close()
          return (json.JSONEncoder().encode(result))
#myjson={"ClicksCounter":4}
#obj=SaveLogs(myjson,"katulentwa@gmail.com")
#result=obj.saveLogsInDB()
#print result
