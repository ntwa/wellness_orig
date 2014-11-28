#!/usr/bin/env python
import datetime
import sys
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.health_goal_module import HealthGoal,ActivityGoal,db
import json

class SaveActivityGoal:
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id
          
     def saveGoal(self):
          
          #myjson = json.load(sys.stdin)
          
          allow_insert=1
          #print "Content-type: application/json"
          # Get data from fields
          result={}
          try:
               steps=self.myjson["stepsGoal"] 
               #duration=self.myjson["targetDuration"] 
               #steps=6000
               #duration="Weekly"
          except Exception as e:
               #print "Content-type: text/html\n" 
               #print "Content-type: application/json"
               result["message"]='There was an error in processing a JSON object'
               #print      
               return (json.JSONEncoder().encode(result))     
               #sys.exit() 
          
          #if (steps=="None"):
          #     print "Content-type: text/html\n" 
          #     print "Error: You have specified details about the goal"
          #     sys.exit()
               
          date_captured = datetime.date.today()    
          
          
          #print "Content-Type: text/html\n"
          
          
          
          
          
          #insert          
          try:
                    #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                    engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    
                    # querying for a record in the physical_activity pattern table
                    res= session.query(HealthGoal,ActivityGoal).filter(HealthGoal.id==ActivityGoal.health_goal_id).filter(HealthGoal.beneficiary_id==self.b_id).filter(HealthGoal.datecaptured==date_captured).filter(HealthGoal.goaltype=="Activities").first()
                    if res is None:
                              pass
                    else:
                              healthgoal,activitygoal=res
                              activitygoal.steps=steps
                              #healthgoal.duration=duration
                    
                              
                              allow_insert=0
                              #size=size-1 #ignore the last value because it has arleady been updated
                              
                    session.commit()
                             
                         
                    
                    
          except Exception as e:
                    #print "Content-type: text/html\n" 
                    session.close()
                    engine.dispose() 
                    result["message"]="There was an error"
                    #print      
                    return (json.JSONEncoder().encode(result))
                    #sys.exit()
          
          
          
          
          
          if allow_insert==1:
                    #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                    # create a Session
                    #Session = sessionmaker(bind=engine)
          
                    #session = Session()
          
                    # Create goal
                    try:
                        
                        
                        new_health_goal=HealthGoal(self.b_id,date_captured,"Activity")
                        new_activity_goal=ActivityGoal(steps)
          
                        new_health_goal.activitygoal=[new_activity_goal]
          
          
                       # Add the record to the session object
          
                        session.add(new_health_goal)
                        session.commit()
                        result["message"]="The goal was set successfully"
                    except Exception as e:
                        result["message"]="The following error occured, %s"%e.message
                        pass
          
          
                    # commit the record the database
          
          
        
          session.close()
          engine.dispose()
         
          
          #print      
          return (json.JSONEncoder().encode(result))
#myjson={"stepsGoal":10000,"targetDuration":"Weekly"} 
#obj=SaveActivityGoal(myjson,8)
#msg=obj.saveGoal()
#print msg
