#!/usr/bin/env python
import datetime
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.weight_module import Weight,db,dbconn
from collections import OrderedDict


class RetrieveWeight:
                 
          def __init__(self,myjson,b_id):
                    self.myjson=myjson
                    self.b_id=b_id
                   
          def getWeight(self):
          
                    errorcode={}
                    result={}
                    beneficiary_id=self.b_id
                    # Get data from fields
                    try:
                              recordeddate=self.myjson["DateCaptured"]
                              #recordeddate=datetime.date(2014,02,13)
                    except Exception:
                              errorcode["error"]=-1
                 
                              return(json.JSONEncoder().encode(errorcode))         
               
          
         
               
                    try:
                                             
                              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                              engine=db
                              # create a Session
                              Session = sessionmaker(bind=engine)
                                                  
                              session = Session()
                                               
                                                  
                             
                              res = session.query(Weight).filter(Weight.beneficiary_id==beneficiary_id).filter(Weight.datecaptured==recordeddate).first()
                              if res is None:
                                        result["weight"]=0
                              else:
                                        weight=res.weight                    
                                        result["weight"]=weight   
                                                  
                                                    
                                                          
                                                                             
                                      
                              session.close()   
                              engine.dispose()
                              dbconn.close()
                              return(json.JSONEncoder().encode(result))
                                                  
                    except Exception as e:
                              session.close()
                              engine.dispose()
                              dbconn.close() 
                              result["weight"]=-1 
                              
                              return (json.JSONEncoder().encode(result))                      


obj=RetrieveWeight({"DateCaptured":"Last month"},8)
msg=obj.getWeight()
print msg
