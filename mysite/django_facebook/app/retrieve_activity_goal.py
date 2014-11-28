#!/usr/bin/env python
import datetime
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.health_goal_module import HealthGoal,ActivityGoal,db,dbconn
import json

class RetrieveActivityGoal:
          def __init__(self,b_id):
                    self.b_id=b_id
          
          def getGoal(self):
                    
                    try:
                              beneficiary_id=self.b_id  
                                                  
                              result_tuple={}                              
                              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                              engine=db
                              # create a Session
                              Session = sessionmaker(bind=engine)
                              session = Session()
                              
                              # querying for a record in the physical_activity pattern table
                              res = session.query(HealthGoal,ActivityGoal).filter(HealthGoal.id==ActivityGoal.health_goal_id).filter(HealthGoal.beneficiary_id==beneficiary_id).filter(HealthGoal.goaltype=="Activity").order_by(HealthGoal.datecaptured.desc()).order_by(HealthGoal.id.desc()).first()
                              
                              if res is None:
                                        result_tuple["Steps"]=-4
                                        #result_tuple["Duration"]="None"                    
                              else:
                                        healthgoal,activitygoal=res                    
                                        steps=activitygoal.steps
                                    
                                        result_tuple["Steps"]=steps
                                        #result_tuple["Duration"]=duration
                                        #size=size-1 #ignore the last value because it has arleady been updated
                              

                                        
                              
                    except Exception as e:
                              
                              #print "Content-type: application/json"
                              result_tuple["Steps"]=-1
                              #result_tuple["Duration"]="Error"
                              #sys.exit()
                     
                    session.close()
                    engine.dispose()    
                    dbconn.close()

                    return (json.JSONEncoder().encode(result_tuple))
#obj=RetrieveActivityGoal(11)
#goal=obj.getGoal()
#print goal
