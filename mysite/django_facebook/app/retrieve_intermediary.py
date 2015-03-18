#!/usr/bin/env python
import datetime
import sys,json
from sqlalchemy import create_engine,distinct,func
from sqlalchemy.orm import sessionmaker
from wellness.applogic.intermediary_module import Intermediary,Beneficiary,db
from collections import OrderedDict


class RetrieveIntermediary:
     def __init__(self,myjson):
          self.myjson=myjson
          self.count=0
     def saveTeamName(self):
          result={}
          try:
              
               beneficiary_id=self.myjson["BeneficiaryID"]
               teamname=self.myjson["TeamName"]
                                  
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["D0"]="Error%s"%e.message
               result["D1"]=-1
               return (json.JSONEncoder().encode(result))
          
          
                   
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               
               
               # querying for a beneficiary
               #res= session.query(Intermediary,Beneficiary).filter(Intermediary.intermediary_id==Beneficiary.intermediary_id).all()
               res= session.query(Beneficiary).filter(Beneficiary.id==beneficiary_id).first()
             
               if res is None:
                    counter=0
               else: 
                    res.team_name=teamname
                    session.commit()
                    result["D0"]="Team name was updated successfully"
                    result["D1"]=1
            
               session.close()
               engine.dispose()
               
               

               return(json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
     
                                   
                                   
          except Exception as e:
                         
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()
                                   
               result["D0"]=e
               result["D1"]=-1
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
          
          
     
     def countIntermediaries(self):
          result={}              
          
          counter=0
          intermediary_records={}          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               data={}
               intermediaries_ids=[]
               # querying for intermediaries who have been assigned beneficiaries
               #res= session.query(Intermediary,Beneficiary).filter(Intermediary.intermediary_id==Beneficiary.intermediary_id).all()
               res= session.query(func.count(Intermediary.intermediary_id).label("count_interm")).filter(Intermediary.intermediary_id==Beneficiary.intermediary_id).first()
             
               if res.count_interm is None:
                    counter=0
               else: 
                    counter=res.count_interm
               
               result["counter"]=counter

               return(json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
     
                                   
                                   
          except Exception as e:
                         
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()
                                   
               intermediary_records["R00"]=e
               #print      
               return (json.JSONEncoder().encode(intermediary_records))
               #sys.exit()
          
          

     def isAssignedBeneficiary(self):
          result={}
          try:
              
               intermediary_id=self.myjson["Username"]
                                  
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error%s"%e.message
               return (json.JSONEncoder().encode(result))
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(Intermediary,Beneficiary).filter(Intermediary.intermediary_id==Beneficiary.intermediary_id).filter(Beneficiary.intermediary_id==intermediary_id).first()
               if res is None:
                    result["message"]="This intermediary is not yet assigned a Beneficary."
               else: 
                    interm,ben=res
                    result["message"]="This intermediary is arleady assigned a Beneficiary. Continuing with this intermediary will override details of an existing beneficiary"
                    result["Fname"]=ben.beneficiary_fname
                    result["Lname"]=ben.beneficiary_lname
                    result["Mobile"]=ben.beneficiary_mobile
                    result["Id"]=ben.id
                    result["Relation"]=ben.relation
                    result["TeamName"]=ben.team_name
                    result["Ifname"]=interm.intermediary_fname
                    result["Ilname"]=interm.intermediary_lname
                                   
               session.close()
               engine.dispose()
                    
               return (json.JSONEncoder().encode(result))                   
                                   
          except Exception as e:
               session.close()
               engine.dispose() 
                         
               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
          

               
     def retrieveOneIntermediaryDetail(self):       
          result={}              
          
          counter=0
          intermediary_record={}
          try:
              
               intermediary_id=self.myjson["Username"]
                                  
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error%s"%e.message
               return (json.JSONEncoder().encode(result))
          
               
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               data={}
               intermediaries_ids=[]
               # querying for intermediaries who have been assigned beneficiaries
               res= session.query(Intermediary).filter(Intermediary.intermediary_id==intermediary_id).first()
                    
                                        
     
               data={}
               found=0
               
               if res is None:
                    pass
               else:
  
                              
                    
                    data["D0"]="%s %s"%(res.intermediary_fname,res.intermediary_lname)      
                    data["D1"]="%s"%res.intermediary_id   
               
                    
          
               intermediary_record["R00"]=data         
               data={}
                         
                                             
                    
                    
               session.close()
               engine.dispose()
               return(json.JSONEncoder().encode(OrderedDict(sorted(intermediary_record.items(), key=lambda t: t[0]))))
     
                                   
                                   
          except Exception as e:
                         
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()
                                   
               intermediary_record["R00"]=e
               #print      
               return (json.JSONEncoder().encode(intermediary_records))
               #sys.exit()

          
          
          
          
     def retrieveIntermediaryInDB(self):       
          result={}              
          
          counter=0
          intermediary_records={}          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               data={}
               intermediaries_ids=[]
               # querying for intermediaries who have been assigned beneficiaries
               res= session.query(Intermediary,Beneficiary).filter(Intermediary.intermediary_id==Beneficiary.intermediary_id).all()
               
               for interm_tuple,ben_tuple in res:
                    if counter<10:
                         Key1="R0"
                    else:
                         Key1="R"
                    
                    data["D0"]="%s %s"%(interm_tuple.intermediary_fname,interm_tuple.intermediary_lname)      
                    data["D1"]="%s"%interm_tuple.intermediary_id   
                    data["D2"]="%s %s. Mobile:%s"%(ben_tuple.beneficiary_fname,ben_tuple.beneficiary_lname,ben_tuple.beneficiary_mobile)
                    data["D3"]="Relationship:%s"%ben_tuple.relation
                    data["D4"]="Gender:%s"%ben_tuple.gender
                    data["D5"]="Mobile:%s"%interm_tuple.mobile # an intermediary's phone number
                    #data["D6"]="Team Name:%s"%ben_tuple.team_name
                    
                    intermediary_records["%s%s"%(Key1,counter)]=OrderedDict(sorted(data.items(), key=lambda t: t[0]))
                                       
                    intermediaries_ids.append(ben_tuple.intermediary_id)
                    counter=counter+1
                    
                    data={}
                    
                    
                    #res= session.query(Intermediary,Beneficiary).filter(Intermediary.intermediary_id not in Beneficiary.intermediary_id).all()
               res= session.query(Intermediary).all()
                    
                                        
               prevcounter=counter
               data={}
               found=0
               for interm_tuple in res:
                         
                    if counter<10:
                         Key1="R0"
                    else:
                         Key1="R"
                              
                    if prevcounter>=0:
                              
                         #for intermediary_id in intermediaries_ids:
                         #     print intermediary_id,interm_tuple.intermediary_id
                         #     if intermediary_id==interm_tuple.intermediary_id:
                         #          print "Break"
                         #          found=1
                         #          break;
                         #if found ==0:
                         if interm_tuple.intermediary_id not in intermediaries_ids:
                              data["D0"]="%s %s"%(interm_tuple.intermediary_fname,interm_tuple.intermediary_lname)      
                              data["D1"]="%s"%interm_tuple.intermediary_id   
                              data["D2"]="None"
                              intermediary_records["%s%s"%(Key1,counter)]=OrderedDict(sorted(data.items(), key=lambda t: t[0]))
                              
                              counter=counter+1
                                   
                         data={}
                         found=0
                                             
                    
                    
               session.close()
               engine.dispose()
               return(json.JSONEncoder().encode(OrderedDict(sorted(intermediary_records.items(), key=lambda t: t[0]))))
     
                                   
                                   
          except Exception as e:
                         
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()
                                   
               intermediary_records["R00"]=e
               #print      
               return (json.JSONEncoder().encode(intermediary_records))
               #sys.exit()
                                         
     
     
#myjson={'Fname':'Lucas','Lname':'Katule','Username':'katulentwa@hotmail.com'}
#obj=RetrieveIntermediary(myjson)
#result=obj.countIntermediaries()
#print result

#myjson={'Fname':'Lucas','TeamName':'Bafana','BeneficiaryID':'1'}
#obj=RetrieveIntermediary(myjson)
#result=obj.saveTeamName()
#print result
