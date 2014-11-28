#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.weight_module import Weight,db,dbconn


class SaveWeight:
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id
     def saveWeightInDB(self):
          beneficiary_id=self.b_id        
          datecaptured=""
          weight=""
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               weight=self.myjson["Weight"] 
               datecaptured=self.myjson["DateCaptured"]
                        
                             
          except Exception:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object'
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          
          
          if(weight=="None") or (datecaptured=="None"):
               #print "Content-type: text/html\n" 
               result["message"]="Error: Some fields are missing. Please fill in both weight and date"
               return (json.JSONEncoder().encode(result)) 
               #sys.exit()
               
          
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(Weight).filter(Weight.beneficiary_id==beneficiary_id).filter(Weight.datecaptured==datecaptured).first()
               if res is None:
                    pass
               else:
                    weightrecord=res
                    previousweight=weightrecord.weight
                    weightrecord.weight=weight
                                
                                             
                    allow_insert=0
                    #size=size-1 #ignore the last value because it has arleady been updated
                    session.commit()
                    result["message"]="The weight for this date existed and it was updated from %s kg to %s kg"%(previousweight,weight)
                                  
                                   
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
                    new_weight=Weight(beneficiary_id,weight,datecaptured)
                         
                    session.add(new_weight)
               
               
                    # commit the record the database
               
               
                    session.commit()
                    result["message"]="The weight was recorded sucessfully"
                    
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
