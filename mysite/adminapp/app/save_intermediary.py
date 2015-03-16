#!/usr/bin/env python
import datetime
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.intermediary_module import Intermediary,db


class SaveIntermediary:
     def __init__(self,myjson):
          self.myjson=myjson
     def saveIntermediaryInDB(self):       
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               fname=self.myjson["Fname"]
               lname=self.myjson["Lname"]
               intermediary_id=self.myjson["Username"]
               mobile=self.myjson["Mobile"]
                        
                             
          except Exception:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object'
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          
          
          if(fname==None) or (lname==None) or (intermediary_id==None):
               #print "Content-type: text/html\n" 
               result["message"]="Error: Some fields are missing. Please fill in both fields"
               return (json.JSONEncoder().encode(result)) 
               #sys.exit()
               
          
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(Intermediary).filter(Intermediary.intermediary_id==intermediary_id).first()
               if res is None:
                    pass
               else:
                    intermediaryrecord=res
                    #previousfname=intermediaryrecord.intermediary_fname
                    intermediaryrecord.intermediary_fname=fname
                    
                    intermediaryrecord.intermediary_lname=lname
                    intermediaryrecord.mobile=mobile
                                
                                                                   
                    allow_insert=0
                    
                    session.commit()
                    result["message"]="The Intermediary's record  was updated sucessfully"
                    
                                   
                                   
          except Exception as e:
                         
               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
                                         
                         
                         
          if allow_insert==1:
               try:
                    #print "Content-Type: text/html\n"
                    engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
               
                    session = Session()
               
                    # Create weight
                    #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                    new_record=Intermediary(intermediary_id,fname,lname,mobile)
                         
                    session.add(new_record)
               
               
                    # commit the record the database
               
               
                    session.commit()
                    result["message"]="The Intermediary record was recorded sucessfully"
               
               except Exception as e:
                    result["message"]=e
                    return (json.JSONEncoder().encode(result)) 
          
                    
          return (json.JSONEncoder().encode(result))
     
     
#myjson={'Fname':'Gwamaka','Lname':'Katule','Username':'gkatule@hotmail.com','Mobile':'0738472538'}
#obj=SaveIntermediary(myjson)
#result=obj.saveIntermediaryInDB()
#print result
