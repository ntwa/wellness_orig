#!/usr/bin/env python
import datetime
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.intermediary_module import Intermediary,Beneficiary,db,dbconn


class SaveBeneficiary:
     def __init__(self,myjson):
          self.myjson=myjson
     def removeBeneficiary(self):
          result={}
          try:

               intermediary_id=self.myjson["Intermediaryid"]
                                  
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]=e.message
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 

          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               
               # querying for a record in the physical_activity pattern table
               res= session.query(Beneficiary).filter(Beneficiary.intermediary_id==intermediary_id).first()
                           
               if res is None:
                    session.commit()
                    result["message"]="The Beneficiary's record doesn't exist hence it can't be deleted"
                    pass
               else:
                    session.delete(res)
                    
                    session.commit()

                    result["message"]="The Beneficiary's record  was deleted sucessfully"
               session.close()
               engine.dispose()    
               dbconn.close()

               return (json.JSONEncoder().encode(result))
                    
                                   
                                   
          except Exception as e:
               session.close()
               engine.dispose()          
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()

     def saveBeneficiaryInDB(self):       
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               fname=self.myjson["Fname"]
               lname=self.myjson["Lname"]
               mobile=self.myjson["Mobile"]
              # b_username=self.myjson["username"]
               intermediary_id=self.myjson["Intermediaryid"]
                                  
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]=e.message
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          
          
          if(fname=="") or (lname=="") or (intermediary_id=="") or (mobile==""):
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
               res= session.query(Beneficiary).filter(Beneficiary.intermediary_id==intermediary_id).first()
                           
               if res is None:
                    session.commit()
                    pass
               else:
                    beneficiaryrecord=res
                    
                    #previousfname=intermediaryrecord.intermediary_fname
                    beneficiaryrecord.beneficiary_fname=fname
                    
                    beneficiaryrecord.beneficiary_lname=lname
                    #beneficiaryrecord.intermediary_id=intermediary_id
                    
                                
                   # beneficiaryrecord.username=b_username
                                             
                    allow_insert=0
                    
                    session.commit()
                    result["message"]="The Beneficiary's record  was updated sucessfully"
                    
                                   
                                   
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
                    new_record=Beneficiary(fname,lname,mobile,intermediary_id)
               
                    session.add(new_record)
                    
               
                    # commit the record the database
               
               
                    session.commit()
                    
                    result["message"]="The Beneficiary's record was recorded sucessfully"
               
               except Exception as e:
                    result["message"]=e
                    return (json.JSONEncoder().encode(result)) 
          session.close()
          engine.dispose()
          dbconn.close()
                    
          return (json.JSONEncoder().encode(result))
     
     
#myjson={'Fname':'Misoti','Lname':'Mkude','Mobile':'0745678909','Intermediaryid':'katulentwa@hotmail.com'}
#obj=SaveBeneficiary(myjson)
#result=obj.removeBeneficiary()
#print result
