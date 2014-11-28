#!/usr/bin/env python
import datetime
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.intermediary_module import Intermediary,Beneficiary,db,dbconn
from collections import OrderedDict


class RetrieveBeneficiary:
     def __init__(self):
          pass
     def retrieveOneBeneficiary(self,intermediary_id):
          try:
               
               engine=db 
              
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               
               # querying for a record in the physical_activity pattern table
               res = session.query(Beneficiary).filter(Beneficiary.intermediary_id==intermediary_id).first()
          
          if res is None:
                    beneficiary_id=None
          else:
                    beneficiary_id=res.id
                    
                    session.commit()
          except Exception as e:
               pass
          
          
          
     def retrieveBeneficiaryInDB(self):       
          result={}              
          
          counter=0
          beneficiary_records={}
          try:
              
               fname=self.myjson["Fname"]
               lname=self.myjson["Lname"]
               mobile=self.myjson["Mobile"]
               intermediary_id=self.myjson["Intermediaryid"]
                                  
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]=e.message
               return (json.JSONEncoder().encode(result))          
          
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               data={}
               # querying for a record in the physical_activity pattern table
               res= session.query(Beneficiary).filter(Beneficiary.intermediary_id==intermediary_id).first()
               
               for ben_tuple in res:
                    if counter<10:
                         Key1="R0"
                    else:
                         Key1="R"
                    
                    data["D0"]="%s %s"%(ben_tuple.beneficiary_fname,ben_tuple.beneficiary_lname)      
                    data["D1"]="%s"%ben_tuple.beneficiary_mobile                   
                    beneficiary_records["%s%s"%(Key1,counter)]=data
               
                    counter=counter+1
                    
                    data={}            
                                             
                    
                    
               session.close()
               engine.dispose()
               dbconn.close()
               return(json.JSONEncoder().encode(OrderedDict(sorted(beneficiary_records.items(), key=lambda t: t[0]))))
     
                                   
                                   
          except Exception as e:
                         
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()
               dbconn.close()                   
               beneficiary_records["R00"]=-1
               #print      
               return (json.JSONEncoder().encode(beneficiary_records))
               #sys.exit()
                                         
     
     
#myjson={'Fname':'Lucas','Lname':'Katule','Username':'katulentwa@gmail.com'}
#obj=RetrieveIntermediary(myjson)
#result=obj.retrieveIntermediaryInDB()
#print result
